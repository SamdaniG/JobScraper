import json
from json import JSONDecodeError

from storage import load_db,save_db

def test_load_db_happy(tmp_path):
    sample={
        "test": "testing",
        "another_test": "meh"
    }

    file_path = tmp_path / "db.json"
    file_path.write_text(json.dumps(sample, indent=4))

    result = load_db(file_path)

    assert result == sample

def test_load_db_failure(tmp_path):
    sample={
        "test": "testing",
        "another_test": "meh"
    }

    file_path = tmp_path / "something.json"
    #file_path.write_text(json.dumps(sample, indent=4))

    result = load_db(file_path)

    assert result == {}

def test_load_db_failure_decode_error(tmp_path):
    file_path = tmp_path / "db.json"
    file_path.write_text("This is not json")

    result = load_db(file_path)

    assert result == {}

def test_save_db(tmp_path):
    file_path = tmp_path / "test.json"
    sample_dict={
        "yo" : "yolo"
    }

    save_db(sample_dict, file_path)

    with open(file_path, "r") as f:
        result= json.load(f)
        #assert json.dumps(sample_dict,indent=4) == f.readlines()

    assert result == sample_dict