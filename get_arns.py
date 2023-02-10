import argparse, json

# Local imports
from github_wrapper import GHWrapper
from lib.logger import AuditLogger
from workflow_regex import find_arns
from pathlib import Path

"""
Goes through a repo workflow object to retrieve ARN 
by doing a regex search on the workflow content.

Output is a dictionary of arns: 
{"workflow.yaml":["arn"]}
"""
def get_arns(repo_workflow):
    arns_result = dict()
    for workflow in repo_workflow:
        workflow_name = workflow['name']
        workflow_content = workflow['content']
        AuditLogger.info(f">> Checking for AWS Role in: {workflow_name}")
        arns = find_arns(workflow_content = workflow_content)
        if arns:
            arns_result = {workflow_name:arns}
    return arns_result

def main():
    # Supporting user provided arguments: type, and scan target.
    parser = argparse.ArgumentParser(description='Identify vulnerabilities in GitHub Actions workflow')
    parser.add_argument('--type',choices=['org','user'],
                        help='Type of entity that is being scanned.')
    parser.add_argument('--target',help='Org or user')
    args = parser.parse_args()
    
    gh = GHWrapper()
    final_result = dict()
    target_type = args.type #org, or user
    target_input = args.target #username of either an org type or user type account
    
    # returns how many repos were found and the repo object for all repos.
    count, repos = gh.get_multiple_repos(target_name=target_input,
                                target_type=target_type)
    AuditLogger.info(f"Metric: Scanning total {count} repos") # printed for metrics.

    for repo_dict in repos:
        AuditLogger.info(f"> Getting all ARNs for {repo_dict}")
        repo_workflows = repos[repo_dict]
        data = get_arns(repo_workflows)
        if data:
            final_result[repo_dict] = data

    if final_result:
        export_directory = Path("scan_results")
        export_directory.mkdir(exist_ok = True, parents = True)
        export_file = (export_directory / f"{args.target}-arns.json")
        export_file.touch(exist_ok = True)
        write_object = json.dumps(final_result,indent=4)
        with open(export_file,"w") as file_writer:
            file_writer.write(write_object)
    else:
        AuditLogger.info(f"No ARNs were found.")

main()