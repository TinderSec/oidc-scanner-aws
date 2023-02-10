import re

# Uses regex library to return of all matches for the given regex.
def find_arns(workflow_content):
    aws_arn_regex = re.compile("arn:aws:iam::\d+:\w+\/\S+")
    return aws_arn_regex.findall(workflow_content)