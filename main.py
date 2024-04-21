import json
import re
import sys

def policy_name_correct(data: dict) -> bool:
    """
    Checks if the 'PolicyName' in the given JSON data is a valid string 
    according to AWS::IAM::Role Policy format.

    Args:
        data (dict): The JSON data to be checked.

    Returns:
        bool: True if the 'PolicyName' is a valid string, False otherwise.
    """
    
    if 'PolicyName' in data:
        policy_name = data['PolicyName'] 
        return type(policy_name) == str and \
            1 <= len(policy_name) <= 128 and \
            bool(re.match(r'[\w+=,.@-]+', policy_name))
    else:
        return False


def policy_document_correct(data: dict) -> bool:
    """
    Checks if the given JSON data contains a valid policy document 
    according to AWS::IAM::Role Policy format. It must contain a 'Statement' key 
    with a list of policy statements.

    Args:
        data (dict): The JSON data to be checked.

    Returns:
        bool: True if the data contains a valid policy document, False otherwise.
    """
    
    if 'PolicyDocument' in data:
        policy_document = data['PolicyDocument']
        return type(policy_document) == dict and \
            'Statement' in policy_document and \
            type(policy_document['Statement']) == list
    else:
        return False


def all_policy_statements_correct(policy_document: dict) -> bool:
    return all([policy_statement_correct(statement) for statement in policy_document['Statement']])

        
def policy_statement_correct(statement: dict) -> bool:
    """
    Checks if a policy statement is correct according to AWS::IAM::Role Policy format. 
    It must contain correct 'Effect', 'Action' and 'Resource' keys.

    Args:
        statement (dict): The policy statement to be checked.

    Returns:
        bool: True if the policy statement is correct, False otherwise.
    """
    
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
        (type(actions) == str and len(actions) > 0) # single action


def all_resources_correct(resources: list | str) -> bool:
    return (type(resources) == list and all([resource_correct(r) for r in resources])) or \
        resource_correct(resources) # single resource


def resource_correct(resource: str) -> bool:
    return type(resource) == str and \
        len(resource) > 0 and \
        not re.match(r'\*', resource) # not an asterisk


def verify(file_path: str) -> bool | None:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return policy_name_correct(data) and \
            policy_document_correct(data) and \
            all_policy_statements_correct(data['PolicyDocument'])
    
    except FileNotFoundError:
        raise Exception(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON format in '{file_path}'.")



if __name__ == '__main__':
    print(verify(sys.argv[1]))
