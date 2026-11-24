"""Reconcile fresh-cycle outputs and populate only explicitly labelled detail fields."""
import csv
import re
from collections import Counter, defaultdict
from openpyxl import load_workbook
from fresh_jobhunt import ROOT, ACTIVE, CATEGORIES, read, save, assess, book, csv_out

def verify():
    meta=ROOT/'data'/'run_metadata';summary=read(meta/'combined_summary.json',{})
    audit={'run_id':summary['run_id'],'portals':{},'potential_cross_source_duplicates':[]}
    groups=defaultdict(list)
    for portal in summary['portals']:
        out=ROOT/'data'/portal;match=ROOT/'data'/'matched_jobs'/portal
        jobs=read(out/f'{portal}_enriched_jobs.json',[])
        if not jobs:raise ValueError(f'No fresh records for {portal}')
        for j in jobs:
            assert j['run_id']==summary['run_id'] and j['source_park']==portal
            assert j['first_collected_at']>='2026-11-19'
            desc=j['full_job_description']
            if j['description_status']=='PAGE_NOT_FOUND' and j['vacancy_status'] in ACTIVE:
                j['vacancy_status']='STATUS_NEEDS_VERIFICATION'
            for field,label in [('job_location','(?:job |work )?location'),('work_arrangement','work (?:mode|arrangement)'),('employment_type','(?:employment|job) type')]:
                m=re.search(r'(?im)^'+label+r'\s*:\s*([^\n]+)',desc)
                if m:j[field]=m[1].strip()
            j['application_instructions']=[s for s in desc.splitlines() if re.search(r'\b(apply|send your|submit your)\b',s,re.I)] or None
            assess(j)
            groups[(re.sub(r'\W+','',j['company_name'].lower()),re.sub(r'\W+','',j['original_job_title'].lower()))].append([portal,j['source_record_id']])
        candidates=[j for j in jobs if j['category']!='NOT RELEVANT']
        save(out/f'{portal}_enriched_jobs.json',jobs)
        save(out/f'{portal}_active_jobs.json',[j for j in jobs if j['vacancy_status'] in ACTIVE])
        for state in ['EXPIRED','CLOSED','STATUS_NEEDS_VERIFICATION','UNKNOWN']:
            save(out/f'{portal}_{state.lower()}.json',[j for j in jobs if j['vacancy_status']==state])
        save(out/f'{portal}_rejected_or_expired.json',[j for j in jobs if j['vacancy_status'] not in ACTIVE or j['category']=='NOT RELEVANT'])
        save(match/f'{portal}_all_matched_jobs.json',candidates);csv_out(match/f'{portal}_all_matched_jobs.csv',candidates);book(match/f'{portal}_all_matched_jobs.xlsx',candidates)
        for suffix,cat in zip(['strong_matches','potential_matches','related_roles','manual_review','expired_relevant'],CATEGORIES[:-1]):book(match/f'{portal}_{suffix}.xlsx',[j for j in candidates if j['category']==cat])
        csv_out(match/f'{portal}_rejected_jobs.csv',[j for j in jobs if j['category']=='NOT RELEVANT'])
        with (match/f'{portal}_all_matched_jobs.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        wb=load_workbook(match/f'{portal}_all_matched_jobs.xlsx');ws=wb['Jobs']
        assert len(rows)==len(candidates)==ws.max_row-1
        assert ws.freeze_panes=='A2' and ws.auto_filter.ref and ws.data_validations.dataValidation
        wb.close();assert len({j['source_record_id'] for j in jobs})==len(jobs)
        report=read(out/'reports'/'collection_report.json',{})
        report.update(category_counts=dict(Counter(j['category'] for j in jobs)),candidate_count=len(candidates),validation_passed=True,
            active=sum(j['vacancy_status'] in ACTIVE for j in jobs),vacancy_status_counts=dict(Counter(j['vacancy_status'] for j in jobs)))
        summary['portals'][portal]=report
        save(out/'reports'/'collection_report.json',report);save(match/'reports'/'matching_report.json',report)
        audit['portals'][portal]={'source':len(jobs),'matched':len(candidates),'formats_agree':True,'identities_unique':True,'timestamps_fresh':True}
    audit['potential_cross_source_duplicates']=[v for v in groups.values() if len({x[0] for x in v})>1]
    summary['candidates']=sum(r['candidate_count'] for r in summary['portals'].values())
    summary['active']=sum(r['active'] for r in summary['portals'].values())
    summary['potential_cross_source_duplicates']=audit['potential_cross_source_duplicates']
    save(meta/'combined_summary.json',summary);save(meta/'source_coverage_report.json',summary['portals']);save(meta/'current_run.json',summary);save(meta/'validation_report.json',audit)
    print(audit)
if __name__=='__main__':verify()
