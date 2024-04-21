# Remitly Internship 2024
### Simple *AWS::IAM::Role Policy* data format verifier

The metod `verify` checks JSON data compliance with the [format](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html) 
and then returns false if an input JSON Resource field contains a single asterisk and true in any other case.
The input is read from a file, which path is required to run the script:


## Run the Script
To execute the script clone the repository and open it on your device. Ensure you have Python 3 (3.11 recomended) installed.
Then open terminal in the repository root directory and run the script by executing the following command:

`python3 main.py <path_to_JSON_file>`

Where `<path_to_JSON_file>` should be an abolute path to the JSON file containing *AWS::IAM::Role Policy* data to be verified, 
for example: `C:\Users\Adam\Documents\input.json`.
Relative path could be used, but the JSON file should be put in the repository root directory prior to the command execution.


## Run Tests
Tests execution requires `pytest` framework installed. 
First, if you don't have it installed, download it via pip3 by running the following command:

`pip3 install pytest`

Then open terminal in the repository root directory and run tests by executing the following command:

`pytest .\test.py -v`

All tests are parametrized and should display the parameters used and results as `-v` flag is run with the command.
