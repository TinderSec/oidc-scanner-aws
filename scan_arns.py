import boto3
from pathlib import Path
import argparse, json

from lib.logger import AuditLogger

def find_vulnerable_arns(target, web_token):
    vulnerabilities = list()
    sts = boto3.client("sts")
    
    # try opening the JSON file containing ARNs found in org's workflows.
    try:
        arn_json = open(f"scan_results/{target}-arns.json")
        arn_json_parsed = json.load(arn_json)
    except:
        AuditLogger.info(f"This ARN file is empty")
        return 0
    for repository in arn_json_parsed:
        for workflow, arn in arn_json_parsed[repository].items():
            for role in arn:
                AuditLogger.info(f">> Attempting to assume {role}")
                try:
                    
                    response = sts.assume_role_with_web_identity(
                        RoleArn=role,
                        RoleSessionName="workflow-oidc-role-scanner",
                        WebIdentityToken=web_token,
                        DurationSeconds=3600
                    )

                    AuditLogger.warn(f"{role} is vulnerable and used in {repository}/{workflow}")
                    vuln_string = {f"{repository}/{workflow}":role}
                    vulnerabilities.append(vuln_string)
                except Exception as e:
                    not_vulnerable = True
                    AuditLogger.error(str(e))
    if len(vulnerabilities) > 0:
        vuln_file = Path('scan_results/vulnerable-arns.json')
        if not vuln_file.exists():
            vuln_file.touch()
        vuln_json_object = json.dumps(vulnerabilities, indent=4)
        with open(vuln_file, 'w') as vuln_file_writer:
            vuln_file_writer.write(vuln_json_object)
    else:
        AuditLogger.info(f"No vulnerabilities were identified in this run")
    
def main():
    parser = argparse.ArgumentParser(description='ARN Scanner.') # setup argument parser object
    parser.add_argument("--token", help = "JWT generated for the job to authenticate in AWS")
    parser.add_argument("--target", help = "Name of the organization being scanned")

    args = parser.parse_args()

    find_vulnerable_arns(args.target, args.token)

main()