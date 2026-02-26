import pytest
#from Waabi_jobs.utils import get_exact_posting_date,get_text_or_none,sha256_hex
#from utils import get_exact_posting_date,get_text_or_none,sha256_hex
from utils import get_exact_posting_date, get_text_or_none, sha256_hex
import hashlib
from datetime import timedelta, date
DATE_FMT = "%a %d-%b-%Y"

def test_sha256_hex():
    word="dsfsdfsdfsvdfg"
    length= 5

    sol=sha256_hex(word,length=length)
    test=hashlib.sha256(word.encode("utf-8")).hexdigest()[:length]

    assert sol==test

def test_get_text_or_none(mocker):
    parent=mocker.Mock()
    elems=mocker.Mock()
    elems.text=" testing   "

    parent.find_elements.return_value=[elems]
    result=get_text_or_none(parent,"by","value")

    assert result == "testing"
    parent.find_elements.assert_called_once_with("by","value")

def test_get_text_or_none_default(mocker):
    parent=mocker.Mock()
    parent.find_elements.return_value=[]

    result=get_text_or_none(parent,"by","value")

    assert result=="meh"
    parent.find_elements.assert_called_once_with("by","value")

def test_get_exact_posting_date(mocker):
    parent=mocker.Mock()
    parent.find_elements.return_value=[]
    mock_date = "Mon 09-Feb-2026"

    result=get_exact_posting_date(parent,"by","value",mock_date)
    assert result == mock_date
    parent.find_elements.assert_called_once_with("by","value")

def test_get_exact_posting_date_30_plus(mocker):
    parent=mocker.Mock()
    elems=mocker.Mock()
    elems.text="posted more than 30+ days ago"
    parent.find_elements.return_value=[elems]
    mock_date = "Mon 09-Feb-2026"

    result=get_exact_posting_date(parent,"by","value",mock_date)
    assert result == mock_date
    parent.find_elements.assert_called_once_with("by","value")

def test_get_exact_posting_date_yesterday(mocker):
    parent = mocker.Mock()
    elems = mocker.Mock()
    elems.text = "posted yesterday ago"
    parent.find_elements.return_value = [elems]
    mock_date = "Mon 09-Feb-2026"

    solution = (date.today() - timedelta(days=1)).strftime(DATE_FMT)
    result = get_exact_posting_date(parent, "by", "value", mock_date)
    assert result == solution
    parent.find_elements.assert_called_once_with("by", "value")

def test_get_exact_posting_date_today(mocker):
    parent = mocker.Mock()
    elems = mocker.Mock()
    elems.text = "posted today"
    parent.find_elements.return_value = [elems]
    mock_date = "Mon 09-Feb-2026"

    solution = (date.today()).strftime(DATE_FMT)
    result = get_exact_posting_date(parent, "by", "value", mock_date)
    assert result == solution
    parent.find_elements.assert_called_once_with("by", "value")

def test_get_exact_posting_date_n_days_ago(mocker):
    parent = mocker.Mock()
    elems = mocker.Mock()
    elems.text = "posted 6 days ago"
    parent.find_elements.return_value = [elems]
    mock_date = "Mon 09-Feb-2026"

    solution = (date.today() - timedelta(days=6)).strftime(DATE_FMT)
    result = get_exact_posting_date(parent, "by", "value", mock_date)
    assert result == solution
    parent.find_elements.assert_called_once_with("by", "value")

def test_get_exact_posting_date_today_patch(mocker):
    mock_date = mocker.patch("utils.date", wraps=date)
    mock_date.today.return_value = date(2026, 2, 9)

    parent = mocker.Mock()
    elem = mocker.Mock()
    elem.text = "posted today"
    parent.find_elements.return_value = [elem]

    result = get_exact_posting_date(parent, "by", "value")

    assert result == "Mon 09-Feb-2026"

def test_get_exact_posting_date_return_check(mocker):
    parent=mocker.Mock()
    elems=mocker.Mock()
    elems.text="random check"
    default_input=date(2026,1,1)

    parent.find_elements.return_value=[elems]

    input=get_exact_posting_date(parent,"by","value",default_input)

    assert input == default_input
    parent.find_elements.assert_called_once_with("by","value")





