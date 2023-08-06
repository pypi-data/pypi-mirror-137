import sys
from os import environ
from .deployer import Executor
import pathlib

import yaml
from botocore.session import Session


INPUT_FILE_ENV = 'DEPLOY_OUTPUT_FILE' # todo file output


def execute_ado_cli():

    expected_env_vars = { INPUT_FILE_ENV }
    missing_vars = []
    for env_var in expected_env_vars:
        if not env_var in environ:
            missing_vars.append(env_var)
    if missing_vars:
        raise Exception(f'Missing environment variables: {missing_vars}')

    cs_result_file_path = environ[INPUT_FILE_ENV]

    cs_result_file_path = pathlib.Path(cs_result_file_path)
    if not cs_result_file_path.exists():
        raise Exception('Stack config file does not exists.')
    cs_result_yaml = cs_result_file_path.read_text()
    cs_result = yaml.safe_load(str(cs_result_yaml))

    stack = execute(
        aws_region=cs_result['stack_region'],
        stack_id=cs_result['changeset']['StackId'],
        changeset_id=cs_result['changeset_id'],
        changeset_type=cs_result['changeset_type'],
    )

    print(yaml.safe_dump(stack))

    if 'Outputs' in stack:
        for output in stack['Outputs']:
            var_name = output['OutputKey']
            var_value = output['OutputValue']
            print(f'##vso[task.setvariable variable={var_name}]{var_value}')


def execute(aws_region, stack_id, changeset_id, changeset_type):

    boto_session = Session()

    cfn_client = boto_session.create_client('cloudformation', region_name=aws_region)

    executor = Executor(cfn_client)
    executor.execute_changeset(changeset_id)
    executor.wait_for_execute(stack_name=stack_id, changeset_type=changeset_type)
    stack = executor.describe_stack(stack_id)
    return stack


if __name__ == '__main__':
    execute_ado_cli()