#from diff import diff_jobs
from diff import diff_jobs
from datetime import  date
#"Thu 01-Jan-2026",
def test_diff_jobs():
    db={
        123 : {
            "filled_date" : ""
        },
        13 :{
            "filled_date" : ""
        }

    }
    current_jobs_id=[123,23,1]

    day = date(2026, 2, 9)

    new_jobs, filled_jobs = diff_jobs(db,current_jobs_id,day)

    assert new_jobs == [23,1]
    assert filled_jobs== [13]
    assert db[13]["filled_date"] == "Sun 08-Feb-2026"

