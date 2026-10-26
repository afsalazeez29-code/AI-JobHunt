from datetime import date
from pathlib import Path

from park_job_reinvestigation import TITLE_KEYWORDS, classify, listed_title_match, normal, phrase_match, skills


def job(title, description="", closing="2026-11-10"):
    return {"source_portal":"Technopark","source_record_id":"1","job_listing_id":"","job_title":title,"company":"Example","posted_date":"","closing_date":closing,"job_description":"","location":"","work_mode":"","job_details_url":"https://example.test/job/1","original_source_record":{}}


def enrichment(text, status="FULL_DESCRIPTION_RETRIEVED"):
    return {"status":status,"text":text,"reason":""}


def test_complete_required_dictionary_is_present_and_normalized():
    assert len(TITLE_KEYWORDS) >= 150
    assert listed_title_match("junior FRONT-END developer")
    assert listed_title_match("React.js Developer")
    assert phrase_match("SDE-1", "SDE 1")
    assert not listed_title_match("Sales Developer Relations Manager")


def test_description_can_discover_relevant_job_without_dictionary_title():
    result=classify(job("Digital Experience Specialist"), enrichment("Build React and Next.js web applications, REST APIs, and responsive user interfaces."))
    assert result["category"] in {"Strong Match","Potential Match","Related Developer Role"}
    assert {"React","Next.js","REST API"}.issubset(set(result["matched_skills"].split(", ")))


def test_relevant_title_without_description_stays_manual_review():
    result=classify(job("Full-Stack Developer"), enrichment("", "FETCH_FAILED"))
    assert result["category"]=="Manual Review" and result["confidence"]=="Low"


def test_expired_candidate_is_preserved_and_eligibility_not_claimed():
    result=classify(job("React Developer",closing="2026-10-20"), enrichment("Required React and a Bachelor's degree."))
    assert result["category"]=="Expired Relevant Role"
    assert result["education_eligibility"]=="Needs Verification"


def test_unrelated_and_required_skill_conflict_behave_transparently():
    rejected=classify(job("Finance Executive"), enrichment("Accounting and finance operations."))
    assert rejected["category"]=="Not Relevant"
    result=classify(job("Java Developer"), enrichment("Required Java, Spring and 4 years experience."))
    assert result["category"]=="Potential Match"
    assert "4 years" in result["experience_requirements"]
