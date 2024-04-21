import json
import re
import sys

def policy_name_correct(data: dict) -> bool:
    if 'PolicyName' in data:
        policy_name = data['PolicyName'] 
        return type(policy_name) == str and \
            1 <= len(policy_name) <= 128 and \
            bool(re.match(r'[\w+=,.@-]+', policy_name))
    else:
        return False


def policy_document_correct(data: dict) -> bool:
    if 'PolicyDocument' in data:
        policy_document = data['PolicyDocument']
        return type(policy_document) == dict and \
            'Statement' in policy_document and \
            type(policy_document['Statement']) == list
    else:
        return False


def all_policy_statements_correct(policy_document: dict) -> bool:
    return all([policy_statement_correct(statement) for statement in policy_document['Statement']])
        
def policy_statement_correct(statement) -> bool:
    if 'Effect' in statement and 'Action' in statement and 'Resource' in statement:
        return effect_correct(statement['Effect']) and \
            all_actions_correct(statement['Action']) and \
            all_resources_correct(statement['Resource'])
    else:
        return False

def effect_correct(effect: str) -> bool:
    return type(effect) == str and \
        effect in ['Allow', 'Deny']
        
def all_actions_correct(actions: list | str) -> bool:
    return (type(actions) == list and all([type(a) == str for a in actions])) or \
        (type(actions) == str and len(actions) > 0)

def all_resources_correct(resources: list | str) -> bool:
    return (type(resources) == list and all([resource_correct(r) for r in resources])) or \
        resource_correct(resources)

def resource_correct(resource: str) -> bool:
    return type(resource) == str and \
        len(resource) > 0 and \
        not re.match(r'\*', resource)


def verify(file_path: str) -> bool | None:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return policy_name_correct(data) and \
            policy_document_correct(data) and \
            all_policy_statements_correct(data['PolicyDocument'])
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None



if __name__ == '__main__':
    print(verify(sys.argv[1]))
