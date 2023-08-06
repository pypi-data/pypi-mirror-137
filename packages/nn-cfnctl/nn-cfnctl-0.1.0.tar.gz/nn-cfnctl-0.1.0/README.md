# CloudFormation Control

<!-- ABOUT THE PROJECT -->
## About The Project

Cloud Formation Control (cfnctl) is a commandline utility based of the AWS CLI Deploy features.
On top of existing deployment capabilities it adds the ability to specify a configuration file to easily supply the following parameters to your CloudFormation deployment:

* StackName
* AwsRegion
* StackParameters
* StackTags

Supplying your CloudFormation template with a config containing the above parameters, and a set of commandline arguments or environment variables, it makes it easier to deploy CloudFormation templates both from your local development machine as well as a pipeline using the same pipelines and configurations.


### Built With

This project is build using the following tools and frameworks:

* [Python](https://www.python.org/)
* [Boto3](https://github.com/boto/boto3)
* [Typer](https://github.com/tiangolo/typer)
* [Poetry](https://github.com/python-poetry/poetry)

<!-- GETTING STARTED -->
## Getting Started

In order to get started with developing and contributing to this project, follow the steps below.

### Prerequisites

#### pipx (Optional)

This project is build and managed by poetry, the easiest way to install poetry in an isolated environment is using [pipx][pipx-install].

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

#### Poetry

If you installed pipx, you can simply install poetry using the command below:

```sh
pipx install poetry
```

If you did not install pipx, see [Poetry documentation][poetry-install] for installation method for your system.

### Installation

1. Clone the repository
   ```sh
   git clone https://novonordiskit@dev.azure.com/novonordiskit/GITO-HS/_git/aws-cfnctl
   ```
2. Change directory into the cloned repository
   ```sh
   cd aws-cfnctl
   ```
3. Install dependencies into a virtual environment with poetry
   ```sh
   poetry install
   ```
3. Activate virtual environment with poetry
   ```sh
   poetry shell
   ```

<!-- USAGE EXAMPLES -->
## Usage

When installed somewhere on the system included in the systems PATH, the application can be called with `cfnctl`.  
To see all available options for the CLI run:
```sh
cfnctl --help  
```
The `cfnctl` command has two primary subcommands:
* `cfnctl plan`
* `cfnctl apply`

### cfnctl plan

`cfnctl plan` creates a new stack plan, or if the stack already exists, a change set plan for AWS CloudFormation. 
The resulting plan can then be used with `cfnctl apply` to execute the stack / change set and provision it in AWS.  

If you wish to execute the plan immediately, set the `--auto-apply` commandline flag or use the `CFNCTL_AUTO_APPLY = $TRUE`.

The `cfnctl plan` command requires the following options:
* --name "CloudFormation change set name."
* --description "CloudFormation change set description."
* --template "Relative or absolute filepath pointing to CloudFormation template file."
* --config "Relative or absolute filepath pointing to CloudFormation template config file."
* --output "Relative or absolute filepath for resulting change set file."

The following settings can be set optionally:
* --export-stack "Export the Stack ID as an Azure DevOps pipeline variable with this name."
* --export-changeset "Export the change set ID as an Azure DevOps pipeline variable with this name."
* --export-outputs "Exports the stack output as Azure DevOps pipeline variables."
* --auto-apply "If set to true, changeset will be created then executed"

### cfnctl apply

`cfnctl apply` executes a stack plan, or if the stack already exists, executes a change set with AWS CloudFormation. 
The command requires a plan file created with the `cfnctl plan` command.


The `cfnctl plan` command requires the following options:
* --name "CloudFormation change set name."
* --description "CloudFormation change set description."
* --template "Relative or absolute filepath pointing to CloudFormation template file."
* --config "Relative or absolute filepath pointing to CloudFormation template config file."
* --output "Relative or absolute filepath for incoming change set file."

The following settings can be set optionally:
* --export-stack "Export the Stack ID as an Azure DevOps pipeline variable with this name."
* --export-changeset "Export the change set ID as an Azure DevOps pipeline variable with this name."
* --export-outputs "Exports the stack output as Azure DevOps pipeline variables."

### Environment variables

Instead of using commandline parameters, it is possible to configure the `cfnctl plan` and `cfnctl apply` commands using environment variables.

#### PowerShell environment variables

Setting environment variables in PowerShell:

```powershell
$env:CFNCTL_CHANGESET_NAME = "MyChangeSet"
$env:CFNCTL_CHANGESET_DESCRIPTION = "Change Set for my stack"
$env:CFNCTL_TEMPLATE_PATH = "my-cfn-template-file.yml"
$env:CFNCTL_STACK_CONFIG_PATH = "my-cfnctl-config-file.yml"
$env:CFNCTL_PLAN_OUTPUT_PATH = "cfn-output-file.yml"

# Optional
$env:CFNCTL_STACK_ID_EXPORT_VAR = "CFNCTL_STACK_ID"
$env:CFNCTL_CHANGESET_ID_EXPORT_VAR = "CFNCTL_CHANGESET_ID"
$env:CFNCTL_EXPORT_STACK_OUTPUT = $TRUE
$env:CFNCTL_AUTO_APPLY = $TRUE
```

You can validate the values is set correctly in your shell with:
```powershell
Get-Item -Path Env:* | Where-Object {$_.name -like "CFNCTL_*"}
```

#### Bash environment variables

Setting Environment variables in Bash:
```sh
export CFNCTL_CHANGESET_NAME = "MyChangeSet"
export CFNCTL_CHANGESET_DESCRIPTION = "Change Set for my stack"
export CFNCTL_TEMPLATE_PATH = "my-cfn-template-file.yml"
export CFNCTL_STACK_CONFIG_PATH = "my-cfnctl-config-file.yml"
export CFNCTL_PLAN_OUTPUT_PATH = "cfn-output-file.yml"

# Optional
export CFNCTL_STACK_ID_EXPORT_VAR = "CFNCTL_STACK_ID"
export CFNCTL_CHANGESET_ID_EXPORT_VAR = "CFNCTL_CHANGESET_ID"
export CFNCTL_EXPORT_STACK_OUTPUT = true
export CFNCTL_AUTO_APPLY = true
```

You can validate the values is set correctly in your shell with:
```sh
env | grep 'CFNCTL_'
```


<!-- MARKDOWN LINKS & IMAGES -->
[pipx-install]: https://pypa.github.io/pipx/installation/
[poetry-install]: https://python-poetry.org/docs/master/#installing-with-the-official-installer
