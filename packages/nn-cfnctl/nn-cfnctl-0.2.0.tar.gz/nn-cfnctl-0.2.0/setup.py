# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nn_cfnctl']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'boto3>=1.20.39,<2.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['cfnctl = nn_cfnctl.main:app']}

setup_kwargs = {
    'name': 'nn-cfnctl',
    'version': '0.2.0',
    'description': 'CLI Tool for deploying CloudFormation using a YAML based config file for stack and parameter settings.',
    'long_description': '# CloudFormation Control\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\n\nCloud Formation Control (cfnctl) is a commandline utility based of the AWS CLI Deploy features.\nOn top of existing deployment capabilities it adds the ability to specify a configuration file to easily supply the following parameters to your CloudFormation deployment:\n\n* StackName\n* AwsRegion\n* StackParameters\n* StackTags\n\nSupplying your CloudFormation template with a config containing the above parameters, and a set of commandline arguments or environment variables, it makes it easier to deploy CloudFormation templates both from your local development machine as well as a pipeline using the same pipelines and configurations.\n\n\n### Built With\n\nThis project is build using the following tools and frameworks:\n\n* [Python](https://www.python.org/)\n* [Boto3](https://github.com/boto/boto3)\n* [Typer](https://github.com/tiangolo/typer)\n* [Poetry](https://github.com/python-poetry/poetry)\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nIn order to get started with developing and contributing to this project, follow the steps below.\n\n### Prerequisites\n\n#### pipx (Optional)\n\nThis project is build and managed by poetry, the easiest way to install poetry in an isolated environment is using [pipx][pipx-install].\n\n```sh\npython -m pip install --user pipx\npython -m pipx ensurepath\n```\n\n#### Poetry\n\nIf you installed pipx, you can simply install poetry using the command below:\n\n```sh\npipx install poetry\n```\n\nIf you did not install pipx, see [Poetry documentation][poetry-install] for installation method for your system.\n\n### Installation\n\n1. Clone the repository\n   ```sh\n   git clone https://novonordiskit@dev.azure.com/novonordiskit/GITO-HS/_git/aws-cfnctl\n   ```\n2. Change directory into the cloned repository\n   ```sh\n   cd aws-cfnctl\n   ```\n3. Install dependencies into a virtual environment with poetry\n   ```sh\n   poetry install\n   ```\n3. Activate virtual environment with poetry\n   ```sh\n   poetry shell\n   ```\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nWhen installed somewhere on the system included in the systems PATH, the application can be called with `cfnctl`.  \nTo see all available options for the CLI run:\n```sh\ncfnctl --help  \n```\nThe `cfnctl` command has two primary subcommands:\n* `cfnctl plan`\n* `cfnctl apply`\n\n### cfnctl plan\n\n`cfnctl plan` creates a new stack plan, or if the stack already exists, a change set plan for AWS CloudFormation. \nThe resulting plan can then be used with `cfnctl apply` to execute the stack / change set and provision it in AWS.  \n\nIf you wish to execute the plan immediately, set the `--auto-apply` commandline flag or use the `CFNCTL_AUTO_APPLY = $TRUE`.\n\nThe `cfnctl plan` command requires the following options:\n* --name "CloudFormation change set name."\n* --description "CloudFormation change set description."\n* --template "Relative or absolute filepath pointing to CloudFormation template file."\n* --config "Relative or absolute filepath pointing to CloudFormation template config file."\n* --output "Relative or absolute filepath for resulting change set file."\n\nThe following settings can be set optionally:\n* --export-stack "Export the Stack ID as an Azure DevOps pipeline variable with this name."\n* --export-changeset "Export the change set ID as an Azure DevOps pipeline variable with this name."\n* --export-outputs "Exports the stack output as Azure DevOps pipeline variables."\n* --auto-apply "If set to true, changeset will be created then executed"\n\n### cfnctl apply\n\n`cfnctl apply` executes a stack plan, or if the stack already exists, executes a change set with AWS CloudFormation. \nThe command requires a plan file created with the `cfnctl plan` command.\n\n\nThe `cfnctl plan` command requires the following options:\n* --name "CloudFormation change set name."\n* --description "CloudFormation change set description."\n* --template "Relative or absolute filepath pointing to CloudFormation template file."\n* --config "Relative or absolute filepath pointing to CloudFormation template config file."\n* --output "Relative or absolute filepath for incoming change set file."\n\nThe following settings can be set optionally:\n* --export-stack "Export the Stack ID as an Azure DevOps pipeline variable with this name."\n* --export-changeset "Export the change set ID as an Azure DevOps pipeline variable with this name."\n* --export-outputs "Exports the stack output as Azure DevOps pipeline variables."\n\n### Environment variables\n\nInstead of using commandline parameters, it is possible to configure the `cfnctl plan` and `cfnctl apply` commands using environment variables.\n\n#### PowerShell environment variables\n\nSetting environment variables in PowerShell:\n\n```powershell\n$env:CFNCTL_CHANGESET_NAME = "MyChangeSet"\n$env:CFNCTL_CHANGESET_DESCRIPTION = "Change Set for my stack"\n$env:CFNCTL_TEMPLATE_PATH = "my-cfn-template-file.yml"\n$env:CFNCTL_STACK_CONFIG_PATH = "my-cfnctl-config-file.yml"\n$env:CFNCTL_PLAN_OUTPUT_PATH = "cfn-output-file.yml"\n\n# Optional\n$env:CFNCTL_STACK_ID_EXPORT_VAR = "CFNCTL_STACK_ID"\n$env:CFNCTL_CHANGESET_ID_EXPORT_VAR = "CFNCTL_CHANGESET_ID"\n$env:CFNCTL_EXPORT_STACK_OUTPUT = $TRUE\n$env:CFNCTL_AUTO_APPLY = $TRUE\n```\n\nYou can validate the values is set correctly in your shell with:\n```powershell\nGet-Item -Path Env:* | Where-Object {$_.name -like "CFNCTL_*"}\n```\n\n#### Bash environment variables\n\nSetting Environment variables in Bash:\n```sh\nexport CFNCTL_CHANGESET_NAME = "MyChangeSet"\nexport CFNCTL_CHANGESET_DESCRIPTION = "Change Set for my stack"\nexport CFNCTL_TEMPLATE_PATH = "my-cfn-template-file.yml"\nexport CFNCTL_STACK_CONFIG_PATH = "my-cfnctl-config-file.yml"\nexport CFNCTL_PLAN_OUTPUT_PATH = "cfn-output-file.yml"\n\n# Optional\nexport CFNCTL_STACK_ID_EXPORT_VAR = "CFNCTL_STACK_ID"\nexport CFNCTL_CHANGESET_ID_EXPORT_VAR = "CFNCTL_CHANGESET_ID"\nexport CFNCTL_EXPORT_STACK_OUTPUT = true\nexport CFNCTL_AUTO_APPLY = true\n```\n\nYou can validate the values is set correctly in your shell with:\n```sh\nenv | grep \'CFNCTL_\'\n```\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n[pipx-install]: https://pypa.github.io/pipx/installation/\n[poetry-install]: https://python-poetry.org/docs/master/#installing-with-the-official-installer\n',
    'author': 'Henrik Stanley Mortensen',
    'author_email': 'hsmx@novonordisk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
