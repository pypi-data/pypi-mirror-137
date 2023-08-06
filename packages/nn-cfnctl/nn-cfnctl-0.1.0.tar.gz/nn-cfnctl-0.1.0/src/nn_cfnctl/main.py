import typer
import os
import sys
import yaml
from pathlib import Path
from os import environ
from .deploy import deploy_py, execute

app = typer.Typer()


@app.callback()
def callback():
    """
    CloudFormation Control CLI
    """

@app.command("plan")
def plan_cloudformation(
    # Required
    changeset_name:             str = typer.Option(..., "--name", envvar="CFNCTL_CHANGESET_NAME", help="CloudFormation change set name."),
    changeset_description:      str = typer.Option(..., "--description", envvar="CFNCTL_CHANGESET_DESCRIPTION", help="CloudFormation change set description."),
    template_path:              Path = typer.Option(..., "--template", resolve_path=True, envvar="CFNCTL_TEMPLATE_PATH", help="Relative or absolute filepath pointing to CloudFormation template file."),
    config_path:                Path = typer.Option(..., "--config", resolve_path=True, envvar="CFNCTL_STACK_CONFIG_PATH", help="Relative or absolute filepath pointing to CloudFormation template config file."),
    plan_output_path:           Path = typer.Option(..., "--output", envvar="CFNCTL_PLAN_OUTPUT_PATH", help="Relative or absolute filepath for resulting change set file."),
    # Optional
    stack_id_var_name:          str = typer.Option("", "--export-stack", envvar="CFNCTL_STACK_ID_EXPORT_VAR", help="Export the Stack ID as an Azure DevOps pipeline variable with this name."),
    changeset_id_var_name:      str = typer.Option("", "--export-changeset", envvar="CFNCTL_CHANGESET_ID_EXPORT_VAR", help="Export the change set ID as an Azure DevOps pipeline variable with this name."),
    export_variables:           bool = typer.Option(False, "--export-outputs", envvar="CFNCTL_EXPORT_STACK_OUTPUT", help="Exports the stack output as Azure DevOps pipeline variables."),
    auto_apply:                 bool = typer.Option(False, "--auto-apply", envvar="CFNCTL_AUTO_APPLY", help="If set to true, changeset will be created then executed"),
):
    """
    Create a new CloudFormation stack / change set plan based on provided template and config file. 
    """
    # Get config file and convert yaml to python dict
    conf_str = config_path.read_text()
    conf_dict = yaml.safe_load(str(conf_str))

    # Check output filepath
    out_file_path = Path(plan_output_path)
    out_file_folder = out_file_path.parent
    out_file_path = str(out_file_path)
    os.makedirs(out_file_folder, exist_ok=True)

    result = deploy_py(conf_dict, changeset_name, changeset_description, template_path)
    result_yaml = yaml.safe_dump(result)
    print(result_yaml)

    f_out = open(out_file_path, 'w')
    f_out.write(result_yaml)
    f_out.close()

    # If auto apply set to True, execute CloudFormation change set using variables from Plan as input.
    if auto_apply:
        apply_cloudformation(changeset_name, changeset_description, template_path, config_path, plan_output_path, stack_id_var_name, changeset_id_var_name, export_variables, auto_apply)

    # Sets variables in Azure DevOps pipeline if parameters are set
    if changeset_id_var_name and not auto_apply:
        changeset_id = result['changeset_id']
        print(f'##vso[task.setvariable variable={changeset_id_var_name}]{changeset_id}')
    if stack_id_var_name and not auto_apply:
        stack_id = result['changeset']['StackId']
        print(f'##vso[task.setvariable variable={stack_id_var_name}]{stack_id}')

    return result['exit_code']

@app.command("apply")
def apply_cloudformation(
    # Required
    changeset_name:             str = typer.Option(..., "--name", envvar="CFNCTL_CHANGESET_NAME", help="CloudFormation change set name."),
    changeset_description:      str = typer.Option(..., "--description", envvar="CFNCTL_CHANGESET_DESCRIPTION", help="CloudFormation change set description."),
    template_path:              Path = typer.Option(..., "--template", resolve_path=True, envvar="CFNCTL_TEMPLATE_PATH", help="Relative or absolute filepath pointing to CloudFormation template file."),
    config_path:                Path = typer.Option(..., "--config", resolve_path=True, envvar="CFNCTL_STACK_CONFIG_PATH", help="Relative or absolute filepath pointing to CloudFormation template config file."),
    plan_output_path:           Path = typer.Option(..., "--output", envvar="CFNCTL_PLAN_OUTPUT_PATH", help="Relative or absolute filepath for resulting change set file."),
    # Optional
    stack_id_var_name:          str = typer.Option("", "--export-stack", envvar="CFNCTL_STACK_ID_EXPORT_VAR", help="Export the Stack ID as an Azure DevOps pipeline variable with this name."),
    changeset_id_var_name:      str = typer.Option("", "--export-changeset", envvar="CFNCTL_CHANGESET_ID_EXPORT_VAR", help="Export the change set ID as an Azure DevOps pipeline variable with this name."),
    export_variables:           bool = typer.Option(False, "--export-outputs", envvar="CFNCTL_EXPORT_STACK_OUTPUT", help="Exports the stack output as Azure DevOps pipeline variables."),
    auto_apply:                 bool = typer.Option(False, "--auto-apply", envvar="CFNCTL_AUTO_APPLY", help="If set to true, changeset will be created then executed"),
):
    """
    Apply a CloudFormation stack / change set based on provided template and config file. 
    """

    cs_result_file_path = plan_output_path

    cs_result_file_path = Path(cs_result_file_path)
    if not cs_result_file_path.exists():
        raise Exception('Stack config file does not exists.')
    cs_result_yaml = cs_result_file_path.read_text()
    cs_result = yaml.safe_load(str(cs_result_yaml))

    stack_id = cs_result['changeset']['StackId']

    stack = execute(
        aws_region=cs_result['stack_region'],
        stack_id=stack_id,
        changeset_id=cs_result['changeset_id'],
        changeset_type=cs_result['changeset_type'],
    )

    print(yaml.safe_dump(stack))

    if export_variables and 'Outputs' in stack:
        for output in stack['Outputs']:
            var_name = output['OutputKey']
            var_value = output['OutputValue']
            print(f'##vso[task.setvariable variable={var_name}]{var_value}')

    if changeset_id_var_name:
        changeset_id = cs_result['changeset_id']
        print(f'##vso[task.setvariable variable={changeset_id_var_name}]{changeset_id}')
    if stack_id_var_name:
        print(f'##vso[task.setvariable variable={stack_id_var_name}]{stack_id}')
    
    return stack


if __name__ == "__main__":
    typer.run(app)