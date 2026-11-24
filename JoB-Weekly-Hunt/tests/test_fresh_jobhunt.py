import json
from datetime import date
from zipfile import ZipFile
import pytest
from fresh_jobhunt import date_status, extract_detail, assess, book, csv_out, FIELDS, TITLE_KEYWORDS
from reset_generated_data import reset

@pytest.mark.parametrize('posted,deadline,expected',[
 ('2026-10-01','2026-12-01','ACTIVE_OLDER_POSTING'),
 ('2026-11-19','2026-11-20','OPEN_CONFIRMED'),
 ('2026-11-18',None,'STATUS_NEEDS_VERIFICATION'),
 ('2026-11-18','2026-11-18','EXPIRED')])
def test_status(posted,deadline,expected):
 assert date_status(posted,deadline,date(2026,11,19))[0]==expected

def test_description_excludes_navigation():
 html='<nav>React developer</nav><section><h2>Brief Description</h2><p>Sales duties only</p></section>'
 detail=extract_detail(html,'technopark')
 assert 'React' not in detail['full_job_description']
 assert extract_detail('<body>No job</body>','infopark')['description_status']=='DESCRIPTION_NOT_AVAILABLE'

def test_reset_integrity_and_preservation(tmp_path):
 root=tmp_path/'project';folder=root/'data'/'technopark';folder.mkdir(parents=True)
 (folder/'jobs.json').write_text('[1]');(root/'.env').write_text('KEEP');(root/'script.py').write_text('KEEP')
 reset(root)
 assert not (folder/'jobs.json').exists()
 assert (root/'.env').read_text()=='KEEP' and (root/'script.py').read_text()=='KEEP'
 archive=next((tmp_path/'_archives').glob('*.zip'))
 with ZipFile(archive) as z:
  assert z.testzip() is None and z.read('data/technopark/jobs.json')==b'[1]'

def test_reset_rejects_unreviewed_data(tmp_path):
 folder=tmp_path/'data'/'technopark';folder.mkdir(parents=True);(folder/'important.py').write_text('KEEP')
 with pytest.raises(ValueError):reset(tmp_path)
 assert (folder/'important.py').exists()

def test_missing_description_and_unknown_eligibility():
 j=assess({'original_job_title':'React Developer','full_job_description':'',
  'description_status':'FETCH_FAILED','vacancy_status':'STATUS_NEEDS_VERIFICATION'})
 assert j['category']=='MANUAL REVIEW' and j['match_score'] is None and j['eligibility']=='NOT_SPECIFIED'

def test_sales_skill_mentions_do_not_make_developer():
 j=assess({'original_job_title':'Technical Sales','full_job_description':'Sell React software applications to customers.',
 'description_status':'FULL_DESCRIPTION_RETRIEVED','vacancy_status':'OPEN_CONFIRMED'})
 assert j['category']=='NOT RELEVANT'

def test_workbook_and_csv_empty_and_populated(tmp_path):
 from openpyxl import load_workbook
 import csv
 for jobs in [[],[{'source_record_id':'1','review_status':'Not Reviewed','original_job_title':'=FORMULA','run_id':'fresh'}]]:
  book(tmp_path/'jobs.xlsx',jobs);csv_out(tmp_path/'jobs.csv',jobs)
  w=load_workbook(tmp_path/'jobs.xlsx');s=w['Jobs']
  assert s.max_row-1==len(jobs) and s.freeze_panes=='A2' and s.data_validations.dataValidation
  if jobs:assert s.cell(2,FIELDS.index('original_job_title')+1).data_type=='s'
  w.close()
  with (tmp_path/'jobs.csv').open(encoding='utf-8-sig') as f:assert len(list(csv.DictReader(f)))==len(jobs)
 assert len(TITLE_KEYWORDS)>=150

def test_full_pipeline_review_refresh_and_partial_protection(tmp_path,monkeypatch):
 import fresh_jobhunt as engine
 from openpyxl import load_workbook
 monkeypatch.setattr(engine,'ROOT',tmp_path)
 monkeypatch.setattr(engine.time,'sleep',lambda _:None)
 class FakeCollector:
  complete=True
  def __init__(self,*a,**kw):pass
  def collect_all_pages(self,run_id):
   return {'records':[{'job_id':'123','job_title':'React Developer','company_name':'Example',
    'date_posted':'19-11-2026','application_deadline':'20 Nov 2099',
    'job_details_url':'https://infopark.in/company-jobs/details/1/123'}],
    'complete_collection_success':self.complete,'pagination':{'pages_expected':1},'pages_successful':[1],
    'duplicate_count':0,'failed_pages':[] if self.complete else [{'page':2,'error':'Timeout'}]}
 monkeypatch.setattr(engine,'InfoparkCollector',FakeCollector)
 class Response:
  status_code=200
  text='<div class="comp-job-detail"><div class="detail-box">React Developer\nRequired React and TypeScript. Build web applications. Freshers accepted. Develop responsive user interfaces and maintain web applications.</div></div>'
  def raise_for_status(self):pass
 monkeypatch.setattr(engine.requests.Session,'get',lambda *a,**kw:Response())
 first=engine.collect('infopark','test-one',0)
 assert first['status']=='COMPLETE' and first['validation_passed']
 folder=tmp_path/'data'/'matched_jobs'/'infopark';path=folder/'infopark_all_matched_jobs.xlsx'
 wb=load_workbook(path);wb['Jobs']['A2']='Apply';wb['Jobs']['B2']='Keep this note';wb.save(path);wb.close()
 engine.collect('infopark','test-two',0)
 state=json.loads((folder/'review_state.json').read_text())
 assert state['123']==['Apply','Keep this note']
 latest=tmp_path/'data'/'infopark'/'infopark_latest_jobs.json';original=latest.read_bytes()
 FakeCollector.complete=False
 result=engine.collect('infopark','test-three',0)
 assert result['status']=='PARTIAL' and latest.read_bytes()==original
