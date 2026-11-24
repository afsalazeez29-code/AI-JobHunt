"""Fresh collection, evidence-based status and matching; never imports old data."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import shutil
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from infopark_job_collector import InfoparkCollector
from technopark_job_collector import TechnoparkCollector, deduplicate_records, compute_status
from park_job_reinvestigation import TITLE_KEYWORDS, listed_title_match
from kerala_job_matching_engine import SKILL_ALIASES

ROOT = Path(__file__).resolve().parent
BASELINE = '2026-11-19'
ACTIVE = {'OPEN_CONFIRMED', 'ACTIVE_OLDER_POSTING'}
CATEGORIES = ['STRONG MATCH','POTENTIAL MATCH','RELATED DEVELOPER ROLE','MANUAL REVIEW','EXPIRED RELEVANT ROLE','NOT RELEVANT']
WEIGHTS = {'title': 25, 'core_skills': 35, 'duties': 25, 'junior': 15}
SKILLS = {**SKILL_ALIASES, 'HTML': ['html','html5'], 'CSS': ['css','css3'],
          'Java': ['java'], 'PHP': ['php'], 'C#': ['c#'], '.NET': ['.net','dotnet'],
          'Angular': ['angular'], 'Spring': ['spring boot'], 'Selenium': ['selenium'], 'Django': ['django']}
CORE = {'React','Next.js','Node.js','Express.js','JavaScript','TypeScript','HTML','CSS','MongoDB','PostgreSQL','REST API'}
PROFILE = set(SKILL_ALIASES) | {'HTML','CSS'}
FIELDS = ['review_status','review_notes','category','match_score','confidence','source_park','source_record_id',
          'company_name','original_job_title','vacancy_status','posting_recency','posting_date','application_deadline',
          'description_status','eligibility','experience_requirements','educational_requirements','fresher_eligibility',
          'required_skills','preferred_skills','matched_skills','missing_required_skills','match_explanation',
          'official_detail_url','job_location','official_application_url','first_collected_at','last_verified_at','run_id',
          'full_job_description']

def now(): return datetime.now(ZoneInfo('Asia/Kolkata'))
def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name('.'+path.name+'.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8'); temp.replace(path)
def read(path, default): return json.loads(path.read_text(encoding='utf8')) if path.exists() else default
def parse_date(value):
    for fmt in ('%Y-%m-%d','%d-%m-%Y','%d %b %Y','%d %B %Y','%d,%b %Y'):
        try: return datetime.strptime(str(value).strip(),fmt).date()
        except ValueError: pass
    return None
def date_status(posted, deadline, reference, recent_days=14, closed=False):
    p,d = parse_date(posted),parse_date(deadline)
    recency = ('POSTING_DATE_UNKNOWN' if not p else 'NEWLY_POSTED' if str(p)==BASELINE else
               'RECENTLY_POSTED' if 0 <= (reference-p).days <= recent_days else 'OLDER_POSTING')
    state = 'CLOSED' if closed else 'EXPIRED' if d and d<reference else (
        'ACTIVE_OLDER_POSTING' if recency=='OLDER_POSTING' else 'OPEN_CONFIRMED') if d else 'STATUS_NEEDS_VERIFICATION'
    return state, recency
def mentions(text):
    return {k for k,aliases in SKILLS.items() if any(re.search(r'(?<!\w)'+re.escape(a)+r'(?!\w)',text,re.I) for a in aliases)}

def extract_detail(html, portal):
    soup = BeautifulSoup(html,'html.parser')
    if portal=='technopark':
        boxes = [h.parent for h in soup.find_all(['h2','h3']) if h.get_text(' ',strip=True) in ('Brief Description','Preferred Skills')]
    else:
        box = soup.select_one('.comp-job-deatiil .deatil-box, .comp-job-detail .detail-box')
        boxes = [box] if box else []
    texts=[]; links=[]
    for box in boxes:
        for tag in box.select('script,style'): tag.decompose()
        texts.append(box.get_text('\n',strip=True))
        links.extend(a.get('href') for a in box.select('a[href]') if re.search(r'apply|application', a.get_text(' ',strip=True),re.I))
    description='\n'.join(texts)
    return {'full_job_description':description,'description_status': 'FULL_DESCRIPTION_RETRIEVED' if len(description)>150 else
            'PARTIAL_DESCRIPTION_RETRIEVED' if description else 'DESCRIPTION_NOT_AVAILABLE',
            'official_application_url': next((u for u in links if u.startswith(('https://','mailto:'))),None)}

def assess(job):
    title=job['original_job_title']; desc=job['full_job_description']; combined=title+'\n'+desc
    hits=listed_title_match(title); overlap=mentions(combined)&PROFILE
    lines=[s.strip() for s in re.split(r'\n|(?<=[.!?])\s+',desc) if s.strip()]
    required=[];preferred=[]; education=[];experience=[]
    for line in lines:
        if re.search(r'\b(preferred|nice to have|bonus|optional)\b',line,re.I): preferred.append(line)
        elif re.search(r'\b(must|required|mandatory|proficien|experience with|strong knowledge)\w*\b',line,re.I): required.append(line)
        if re.search(r'\b(degree|bachelor|b\.?tech|mca|bca|qualification|arrears|backlogs|supplementary)\b',line,re.I): education.append(line)
        if re.search(r'\b\d+\s*(?:[-–]\s*\d+)?\s*\+?\s*(?:years?|yrs?)\b',line,re.I): experience.append(line)
    duties=[s for s in lines if re.search(r'(develop|build|implement|design|maintain)\w*.{0,65}(software|application|frontend|front.end|backend|web|api|interface)',s,re.I)]
    unrelated=bool(re.search(r'\b(sales|marketing|recruitment|accountant|hr|legal|business development)\b',title,re.I))
    developer=bool(hits or re.search(r'\b(developer|programmer|software|frontend|backend|full.stack)\b',title,re.I))
    candidate=developer or bool(duties and overlap & CORE and not unrelated)
    req_skills=mentions('\n'.join(required)); missing=req_skills-PROFILE
    years=[int(n) for s in experience for n in re.findall(r'(\d+)\s*(?:[-–]\s*\d+)?\s*\+?\s*(?:years?|yrs?)',s,re.I)]
    junior=bool(re.search(r'\b(freshers?|entry.level|internship|trainee)\b',combined,re.I))
    # Do not score generic company technology portfolios as vacancy requirements.
    overlap=mentions(title+'\n'+'\n'.join(required+preferred+duties))&PROFILE
    points={'title': WEIGHTS['title'] if developer else 0,
            'core_skills': min(WEIGHTS['core_skills'],len(overlap&CORE)*7),
            'duties': WEIGHTS['duties'] if duties else 0,'junior':WEIGHTS['junior'] if junior else 0}
    score=sum(points.values()); full=job['description_status']=='FULL_DESCRIPTION_RETRIEVED'
    if unrelated or not candidate: category='NOT RELEVANT'
    elif job['vacancy_status'] in {'EXPIRED','CLOSED'}: category='EXPIRED RELEVANT ROLE'
    elif not full: category='MANUAL REVIEW'
    elif score>=75 and not missing and not any(y>1 for y in years) and not re.search(r'\b(senior|lead|architect|principal)\b',title,re.I): category='STRONG MATCH'
    elif len(overlap&CORE)>=2: category='POTENTIAL MATCH'
    else: category='RELATED DEVELOPER ROLE'
    job.update(category=category,match_score=score if full else None,score_components=points,
        confidence='Medium' if full else 'Low',matched_skills=sorted(overlap),required_skills=sorted(req_skills),
        preferred_skills=sorted(mentions('\n'.join(preferred))),missing_required_skills=sorted(missing),
        responsibilities=duties,experience_requirements=experience,educational_requirements=education,
        fresher_eligibility='Explicit fresher/entry wording: verify context' if junior else 'Not specified',
        eligibility='NEEDS_VERIFICATION' if education or experience or missing else 'NOT_SPECIFIED',
        match_explanation=f'Title evidence: {hits[:3]}; profile skills: {sorted(overlap)}; development-duty excerpts: {duties[:2]}. '
            'Education and professional employment are not established by project experience.',
        evidence={'required_excerpts':required,'preferred_excerpts':preferred})
    return job

def csv_out(path, jobs, fields=FIELDS):
    tmp=path.with_name('.'+path.name+'.tmp')
    with tmp.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for j in jobs:w.writerow({k:json.dumps(j.get(k),ensure_ascii=False) if isinstance(j.get(k),(dict,list)) else j.get(k) for k in fields})
    tmp.replace(path)
def book(path,jobs):
    wb=Workbook(); ws=wb.active;ws.title='Jobs';ws.append(FIELDS)
    for j in jobs:
        ws.append([json.dumps(j.get(k),ensure_ascii=False) if isinstance(j.get(k),(dict,list)) else j.get(k) for k in FIELDS])
        for c in ws[ws.max_row]:
            if isinstance(c.value,str):c.data_type='s'
        if j.get('official_detail_url'):ws.cell(ws.max_row,FIELDS.index('official_detail_url')+1).hyperlink=j['official_detail_url']
    for c in ws[1]: c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='1F4E78')
    for row in ws:
        for c in row:c.alignment=Alignment(wrap_text=True,vertical='top')
    for i,k in enumerate(FIELDS,1):ws.column_dimensions[get_column_letter(i)].width=40 if k in {'original_job_title','match_explanation','full_job_description','review_notes'} else 23
    ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
    dv=DataValidation(type='list',formula1='"Not Reviewed,Apply,Review,Skip,Applied"');ws.add_data_validation(dv);dv.add(f'A2:A{max(2,ws.max_row)}')
    tmp=path.with_name('.'+path.name+'.tmp');wb.save(tmp);wb.close();tmp.replace(path)

def collect(portal,run_id,delay):
    out=ROOT/'data'/portal; out.mkdir(parents=True,exist_ok=True)
    if portal=='technopark':
        client=TechnoparkCollector(out,delay=delay); result=client.collect(run_id)
        records,dedupe=deduplicate_records(result.raw_records); state,reasons=compute_status(result,len(records))
        report={'status':state,'pages_discovered':(result.first_payload or {}).get('last_page'),
          'pages_processed':sum(p.success for p in result.page_results),'unique':len(records),
          'duplicates':dedupe['duplicate_occurrences'],'errors':reasons,'pages':[p.report_entry() for p in result.page_results]}
    else:
        client=InfoparkCollector(ROOT,delay=delay); r=client.collect_all_pages(run_id)
        records=r.pop('records');report={'status':'COMPLETE' if r['complete_collection_success'] else 'PARTIAL',
            'pages_discovered':r['pagination']['pages_expected'],'pages_processed':len(r['pages_successful']),
            'unique':len(records),'duplicates':r['duplicate_count'],'errors':r['failed_pages'],'collector_report':r}
    save(out/'reports'/'collection_report.json',report)
    save(out/'raw'/f'{run_id}.json',records)
    if report['status']!='COMPLETE':return report
    save(out/f'{portal}_latest_jobs.json',records)
    csv_out(out/f'{portal}_latest_jobs.csv',records,sorted({k for j in records for k in j}))
    session=requests.Session();session.headers['User-Agent']='JobHunt/2.0 public vacancy review'
    session.mount('https://',HTTPAdapter(max_retries=Retry(total=2,backoff_factor=1,status_forcelist=[429,500,502,503,504],respect_retry_after_header=True)))
    old={j['source_record_id']:j for j in read(out/f'{portal}_enriched_jobs.json',[])}
    cache_path=out/'detail_cache.json';cache=read(cache_path,{})
    enriched=[];started=now().isoformat()
    for idx,raw in enumerate(records):
        identity=str(raw.get('id',raw.get('job_id','')) or f'missing-{idx}')
        url=f'https://technopark.in/job-details/{identity}' if portal=='technopark' else raw.get('job_details_url')
        timestamp=now().isoformat();cached=cache.get(identity,{})
        detail={'full_job_description':'','description_status':'FETCH_FAILED','official_application_url':None}
        try:
            if cached.get('url')==url and cached.get('run_id')==run_id:detail=cached['detail']
            else:
                time.sleep(delay); response=session.get(url,timeout=(10,30))
                if response.status_code==404:detail['description_status']='PAGE_NOT_FOUND'
                elif response.status_code in (401,403):detail['description_status']='ACCESS_RESTRICTED'
                else:response.raise_for_status();detail=extract_detail(response.text,portal)
        except requests.RequestException as e:detail['error']=str(e)
        cache[identity]={'url':url,'run_id':run_id,'detail':detail,'verified_at':timestamp}
        job={'source_park':portal,'source_record_id':identity,'original_source_record':raw,
             'company_name':(raw.get('company') or {}).get('company') if portal=='technopark' else raw.get('company_name'),
             'original_job_title':raw.get('job_title',''),'normalized_job_title':re.sub(r'\W+',' ',raw.get('job_title','').lower()),
             'posting_date':raw.get('posted_date',raw.get('date_posted')),'last_modified_date':raw.get('updated_at'),
             'application_deadline':raw.get('closing_date',raw.get('application_deadline')),
             'listing_url':'https://technopark.in/job-search' if portal=='technopark' else 'https://infopark.in/companies-job',
             'official_detail_url':url,'job_location':None,'campus':None,'employment_type':None,'work_arrangement':None,
             'application_instructions':None,'source_status':None,'first_collected_at':old.get(identity,{}).get('first_collected_at',started),
             'last_verified_at':timestamp,'run_id':run_id,**detail}
        job['vacancy_status'],job['posting_recency']=date_status(job['posting_date'],job['application_deadline'],now().date(),
            closed=bool(re.search(r'applications? (?:are |is )?closed|vacancy (?:is )?closed',job['full_job_description'],re.I)))
        if job['description_status']=='PAGE_NOT_FOUND' and job['vacancy_status'] in ACTIVE:
            job['vacancy_status']='STATUS_NEEDS_VERIFICATION'
        enriched.append(assess(job))
        if (idx+1)%25==0:save(cache_path,cache);print(f'{portal}: descriptions {idx+1}/{len(records)}',flush=True)
    save(cache_path,cache)
    matchdir=ROOT/'data'/'matched_jobs'/portal;matchdir.mkdir(parents=True,exist_ok=True)
    review=read(matchdir/'review_state.json',{})
    # Read every editable view; one changed value wins, conflicting edits stop safely.
    changes={}
    for path in matchdir.glob('*.xlsx'):
        wb=load_workbook(path,read_only=True);ws=wb['Jobs'];heads=[c.value for c in ws[1]]
        for values in ws.iter_rows(min_row=2,values_only=True):
            row=dict(zip(heads,values));identity=str(row['source_record_id']);value=[row.get('review_status') or '',row.get('review_notes') or '']
            if value!=review.get(identity,['Not Reviewed','']):
                if identity in changes and changes[identity]!=value:raise ValueError(f'Conflicting workbook reviews for {identity}')
                changes[identity]=value
        wb.close()
        backup=matchdir/'review_backups'/run_id;backup.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup/path.name)
    review.update(changes)
    for j in enriched:
        j['review_status'],j['review_notes']=review.setdefault(j['source_record_id'],['Not Reviewed',''])
    save(matchdir/'review_state.json',review)
    active=[j for j in enriched if j['vacancy_status'] in ACTIVE]
    candidates=[j for j in enriched if j['category']!='NOT RELEVANT']
    save(out/f'{portal}_enriched_jobs.json',enriched);save(out/f'{portal}_active_jobs.json',active)
    save(out/f'{portal}_rejected_or_expired.json',[j for j in enriched if j['vacancy_status'] not in ACTIVE or j['category']=='NOT RELEVANT'])
    for state in ['EXPIRED','CLOSED','STATUS_NEEDS_VERIFICATION','UNKNOWN']:save(out/f'{portal}_{state.lower()}.json',[j for j in enriched if j['vacancy_status']==state])
    save(matchdir/f'{portal}_all_matched_jobs.json',candidates);csv_out(matchdir/f'{portal}_all_matched_jobs.csv',candidates)
    book(matchdir/f'{portal}_all_matched_jobs.xlsx',candidates)
    for suffix,cat in zip(['strong_matches','potential_matches','related_roles','manual_review','expired_relevant'],CATEGORIES[:-1]):book(matchdir/f'{portal}_{suffix}.xlsx',[j for j in candidates if j['category']==cat])
    csv_out(matchdir/f'{portal}_rejected_jobs.csv',[j for j in enriched if j['category']=='NOT RELEVANT'])
    with (matchdir/f'{portal}_all_matched_jobs.csv').open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==len(candidates)
    wb=load_workbook(matchdir/f'{portal}_all_matched_jobs.xlsx');assert wb['Jobs'].max_row-1==len(candidates);wb.close()
    assert all(j['run_id']==run_id and j['source_park']==portal for j in enriched)
    report.update(run_id=run_id,completed_at=now().isoformat(),active=len(active),candidate_count=len(candidates),
        vacancy_status_counts=dict(Counter(j['vacancy_status'] for j in enriched)),posting_recency_counts=dict(Counter(j['posting_recency'] for j in enriched)),
        description_counts=dict(Counter(j['description_status'] for j in enriched)),category_counts=dict(Counter(j['category'] for j in enriched)),validation_passed=True)
    save(out/'reports'/'collection_report.json',report);save(matchdir/'reports'/'matching_report.json',report)
    failures=[{'id':j['source_record_id'],'status':j['description_status'],'error':j.get('error')} for j in enriched if j['description_status']!='FULL_DESCRIPTION_RETRIEVED']
    save(out/'reports'/'failures_and_warnings.json',failures)
    return report

def run(portals=None):
    p=argparse.ArgumentParser();p.add_argument('--delay',type=float,default=0.5);args=p.parse_args()
    if args.delay<0:p.error('delay must be nonnegative')
    run_id='jobhunt_'+now().strftime('%Y-%m-%d_%H%M%S%f');meta=ROOT/'data'/'run_metadata'
    save(meta/'current_run.json',{'run_id':run_id,'restart_baseline':BASELINE,'started_at':now().isoformat(),'status':'RUNNING','weights':WEIGHTS,'recency_window_days':14})
    reports={}
    for portal in portals or ['technopark','infopark']:
        try:reports[portal]=collect(portal,run_id,args.delay)
        except Exception as e:reports[portal]={'status':'FAILED','error':str(e)}
        save(meta/'source_coverage_report.json',reports)
    summary={'run_id':run_id,'completed_at':now().isoformat(),'portals':reports,
        'status':'COMPLETE' if all(r['status']=='COMPLETE' for r in reports.values()) else 'PARTIAL',
        'total_unique':sum(r.get('unique',0) for r in reports.values()),'active':sum(r.get('active',0) for r in reports.values()),
        'candidates':sum(r.get('candidate_count',0) for r in reports.values())}
    save(meta/'combined_summary.json',summary);save(meta/'current_run.json',summary)
    if summary['status']=='COMPLETE':
        from verify_fresh_jobhunt import verify
        verify()
    print(json.dumps(summary,indent=2),flush=True)
    return 0 if summary['status']=='COMPLETE' else 2
