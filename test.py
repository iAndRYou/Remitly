import json
import main
import pytest

@pytest.mark.parametrize("file, expected", [   
    ('example.json', False),
    ('test/test_correct1.json', True),
    ('test/test_correct2.json', True),
    ('test/test_incorrect1.json', False),
    ('test/test_incorrect2.json', False),
])
def test_policy_json(file, expected):
    assert main.verify(file) == expected


@pytest.mark.parametrize("file, expected", [
    ('test/test_name_correct1.json', True),
    ('test/test_name_incorrect1.json', False),
    ('test/test_name_incorrect2.json', False),
    ('test/test_name_incorrect3.json', False),
])
def test_policy_name(file, expected):
    with open(file, 'r') as f:
        data = json.load(f)
    assert main.policy_name_correct(data) == expected
    

@pytest.mark.parametrize("file, expected", [
    ('test/test_document_correct1.json', True),
    ('test/test_document_incorrect1.json', False),
    ('test/test_document_incorrect2.json', False),
    ('test/test_document_incorrect3.json', False),
])
def test_policy_document(file, expected):
    with open(file, 'r') as f:
        data = json.load(f)
    assert main.policy_document_correct(data) == expected
    

@pytest.mark.parametrize("data, expected", [
    ({'Effect': 'Allow', 'Action': 's3:GetObject', 'Resource': ['arn:aws:s3:::my_corporate_bucket']}, True),
    ({'Effect': 'Allow', 'Action': ['s3:ListBucket', 's3:GetObject'], 'Resource': '*'}, False),
    ({'Effect': 'Deny', 'Action': 's3:ListBucket'}, False),
    ({'Effect': 'Deny', 'Resource': ['arn:aws:s3:::my_corporate_bucket']}, False),
    ({'Effect': 'Deny'}, False),
    ({'Action': ['s3:ListBucket', 's3:GetObject'], 'Resource': ''}, False),
])
def test_policy_statement(data, expected):
    assert main.policy_statement_correct(data) == expected

@pytest.mark.parametrize("data, expected", [
    ('Allow', True),
    ('Deny', True),
    ('Deny ', False),
    ('Forbid', False),
    (1, False),
    ('', False),
])
def test_effect(data, expected):
    assert main.effect_correct(data) == expected
    

@pytest.mark.parametrize("data, expected", [
    (['s3:ListBucket', 's3:GetObject'], True),
    ('s3:ListBucket', True),
    (['s3:ListBucket', 1], False),
    (1, False),
    ('', False),
])
def test_all_actions_correct(data, expected):
    assert main.all_actions_correct(data) == expected
    
    
@pytest.mark.parametrize("data, expected", [
    (['arn:aws:s3:::my_corporate_bucket', 'arn:aws:s3:::unauthorized_bucket'], True),
    ('arn:aws:s3:::my_corporate_bucket', True),
    ('*', False),
    (['arn:aws:s3:::my_corporate_bucket', '*'], False),
    (['arn:aws:s3:::my_corporate_bucket', 1], False),
    (1, False),
    ('', False),
])
def test_all_resources_correct(data, expected):
    assert main.all_resources_correct(data) == expected