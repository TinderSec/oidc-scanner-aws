# GHA OIDC SCANNER - AWS by Tinder Security Labs

## ABOUT

This is a GitHub Action built by Tinder Security Labs as part of public release of research done on configurations for AWS and GHA OIDC setups. This workflow allows organizations to monitor and identify vulnerabilities in their IAM roles through a black-box security approach. 

## Usage
Use the following sample workflow and setup guidellines to setup and run this GHA in your organization. We recommend using this action in a **private** repository. 

### Scanning private repositories
Replace the `${{ github.token }}` with a private PAT if you want to scan private/internal repositories. In order to securely store and use the API key, create a secret and replace `${{ github.token }}` with `${{ secrets.YOUR_SECRET_VAR }}`


### Sample Workflow

```
name: GHA Scanner Action - OIDC
on:
 workflow_dispatch: 

permissions:
  id-token: write
  contents: read

jobs:
  ScanVulns:
    env:
      AWS_REGION: us-east-1
    runs-on: ubuntu-latest
    steps:
      - name: Git clone the repository
        uses: actions/checkout@v1
      - name: Action IP
        run: curl https://ifconfig.me
      - uses: actions/setup-node@v2
      - run: npm install @actions/core@1.6.0-beta.0 
      - run: pip install boto3
      - uses: TinderSec/oidc-scanner-aws@main
        env:
          PAT: ${{ github.token }}
```

## Output

If role(s) are found vulnerable, an artifact will be created in the ran job with `vulnerable-arns.json.zip` file. This zip will include a single JSON file that contains the role name and the associated repository/workflow location. Example JSON file: 

```
[
    {
        "ORG_NAME/REPO_NAME/sample_workflow.yaml": "arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME"
    }
]
```

## License

Copyright © 2022 Match Group, LLC

The copyright holder grants you permission to and use or redistribute this software in source and binary forms, with or without modification, conditioned on your acceptance of, and adherence to, the following conditions:

1.  Redistributions of source code, whether or not modified, must retain the above copyright notice, this list of conditions, and the following disclaimer.  If modified, the source code must identify the modifications (identification in general terms is acceptable).

2.  Redistributions in binary or application form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation or other materials provided with the binary or application.

3.  You may not use the name of the copyright holder nor the names of the contributors to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ALL EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON INFRINGEMENT ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  YOU AGREE TO INDEMNIFY AND HOLD HARMLESS THE COPYRIGHT HOLDER AND ALL CONTRIBUTORS AGAINST ANY CLAIMS THAT ARISE BASED ON YOUR USE, MODIFICATION, OR REDISTRIBUTION OF THIS SOFTWARE.  NO ADDITIONAL LICENSE BEYOND THOSE EXPRESSLY GRANTED ABOVE ARE IMPLIED.