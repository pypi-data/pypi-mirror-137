# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# Modified version of this file:
# https://github.com/aws/aws-cli/blob/develop/awscli/customizations/cloudformation/deploy.py

import os
from os import environ
import sys
import logging
import pathlib

import yaml
from botocore.session import Session

from .exceptions import *
from .deployer import Deployer, Executor
from .yamlhelper import yaml_parse


LOG = logging.getLogger(__name__)


CAPABILITIES = {'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND'}

MSG_EXECUTE_SUCCESS = "Successfully created/updated stack - {stack_name}\n"

MSG_NO_EXECUTE_CHANGESET = \
    ("Changeset created successfully. Run the following command to "
        "review changes:"
        "\n"
        "aws cloudformation describe-change-set --change-set-name "
        "{changeset_id}"
        "\n")


def deploy_py(conf_dict, changeset_name, changeset_description, template_path,
            capabilities=CAPABILITIES, exeute_changeset=False,
            fail_on_empty_changeset=False):
    capabilities = list(capabilities)
    stack_name = conf_dict['StackName']
    aws_region = conf_dict['AwsRegion']
    parameter_overrides = conf_dict['StackParameters']
    tags_dict = conf_dict['StackTags']

    boto_session = Session()
    
    # ---- from _run_main

    cloudformation_client = \
        boto_session.create_client('cloudformation', region_name=aws_region)
        
    if not os.path.isfile(template_path):
        raise InvalidTemplatePathError(
                template_path=template_path)

    # Parse parameters
    with open(template_path, "r") as handle:
        template_str = handle.read()

    tags = [{"Key": key, "Value": value}
                for key, value in tags_dict.items()]
    
    template_dict = yaml_parse(template_str)

    parameters = merge_parameters(template_dict, parameter_overrides)
    
    template_size = os.path.getsize(template_path)
    if template_size > 51200:
        raise DeployBucketRequiredError()

    deployer = Deployer(cloudformation_client, changeset_name, changeset_description)
    return deploy(deployer, stack_name, template_str, aws_region,
                    parameters, capabilities,
                    exeute_changeset, None, None,
                    tags,
                    fail_on_empty_changeset)

def deploy(deployer, stack_name, template_str, aws_region,
            parameters, capabilities, execute_changeset, role_arn,
            notification_arns, tags,
            fail_on_empty_changeset=True):
    try:
        result = deployer.create_and_wait_for_changeset(
            stack_name=stack_name,
            cfn_template=template_str,
            parameter_values=parameters,
            capabilities=capabilities,
            role_arn=role_arn,
            notification_arns=notification_arns,
            tags=tags
        )
    except ChangeEmptyError as ex:
        if fail_on_empty_changeset:
            raise
        changeset = ex.kwargs['changeset']
        deployer.delete_changeset(changeset['ChangeSetId'])
        return {
            'exit_code': 0,
            'status': 'NO_CHANGES',
            'message': 'The ChangeSet contained no changes and has been deleted.',
            'stack_region': aws_region,
            'stack_name': stack_name,
            'changeset_name': deployer.changeset_name,
            'changeset_type': 'NO_CHANGES',
            'changeset_id': changeset['ChangeSetId'],
            'changeset': changeset,
        }

    if execute_changeset:
        deployer.execute_changeset(result.changeset_id, stack_name)
        deployer.wait_for_execute(stack_name, result.changeset_type)
        sys.stdout.write(MSG_EXECUTE_SUCCESS.format(
                stack_name=stack_name))
        status = 'UPDATES_APPLIED'
        message = 'The ChangeSet was executed successfully.'
    else:
        sys.stdout.write(MSG_NO_EXECUTE_CHANGESET.format(
                changeset_id=result.changeset_id))
        status = 'UPDATES_PENDING_APPROVAL'
        message = 'The ChangeSet is pending execution.'

    sys.stdout.flush()
    return {
        'exit_code': 0,
        'status': status,
        'message': message,
        'stack_region': aws_region,
        'stack_name': stack_name,
        'changeset_name': deployer.changeset_name,
        'changeset_type': result.changeset_type,
        'changeset_id': result.changeset_id,
        'changeset': result.changeset,
    }

def merge_parameters(template_dict, parameter_overrides):
    """
    CloudFormation CreateChangeset requires a value for every parameter
    from the template, either specifying a new value or use previous value.
    For convenience, this method will accept new parameter values and
    generates a dict of all parameters in a format that ChangeSet API
    will accept

    :param parameter_overrides:
    :return:
    """
    parameter_values = []

    if not isinstance(template_dict.get("Parameters", None), dict):
        return parameter_values

    for key, value in template_dict["Parameters"].items():

        obj = {
            "ParameterKey": key
        }

        if key in parameter_overrides:
            obj["ParameterValue"] = parameter_overrides[key]
        else:
            obj["UsePreviousValue"] = True

        parameter_values.append(obj)

    return parameter_values


# def execute_ado_cli():

#     expected_env_vars = { env.OUTPUT_FILE_ENV }
#     missing_vars = []
#     for env_var in expected_env_vars:
#         if not env_var in environ:
#             missing_vars.append(env_var)
#     if missing_vars:
#         raise Exception(f'Missing environment variables: {missing_vars}')

#     cs_result_file_path = environ[env.OUTPUT_FILE_ENV]
    
#     export_stack_outputs = env.get_flag(env.OUTPUT_AS_VARIABLES_ENV, False)
#     changeset_id_var_name = env.get_optional_var(env.CHANGESET_ID_VAR_NAME_ENV)
#     stak_id_var_name = env.get_optional_var(env.STACK_ID_VAR_NAME_ENV)

#     cs_result_file_path = pathlib.Path(cs_result_file_path)
#     if not cs_result_file_path.exists():
#         raise Exception('Stack config file does not exists.')
#     cs_result_yaml = cs_result_file_path.read_text()
#     cs_result = yaml.safe_load(str(cs_result_yaml))

#     stack_id = cs_result['changeset']['StackId']

#     stack = execute(
#         aws_region=cs_result['stack_region'],
#         stack_id=stack_id,
#         changeset_id=cs_result['changeset_id'],
#         changeset_type=cs_result['changeset_type'],
#     )

#     print(yaml.safe_dump(stack))

#     if export_stack_outputs and 'Outputs' in stack:
#         for output in stack['Outputs']:
#             var_name = output['OutputKey']
#             var_value = output['OutputValue']
#             print(f'##vso[task.setvariable variable={var_name}]{var_value}')

#     if changeset_id_var_name:
#         changeset_id = cs_result['changeset_id']
#         print(f'##vso[task.setvariable variable={changeset_id_var_name}]{changeset_id}')
#     if stak_id_var_name:
#         print(f'##vso[task.setvariable variable={stak_id_var_name}]{stack_id}')
    
#     return stack


def execute(aws_region, stack_id, changeset_id, changeset_type):

    boto_session = Session()

    cfn_client = boto_session.create_client('cloudformation', region_name=aws_region)

    executor = Executor(cfn_client)
    executor.execute_changeset(changeset_id)
    executor.wait_for_execute(stack_name=stack_id, changeset_type=changeset_type)
    stack = executor.describe_stack(stack_id)
    return stack


# if __name__ == '__main__':

#     options = ['deploy', 'execute']
#     if len(sys.argv) < 2:
#         raise Exception(f'Must give 1 of 2 arguments: {options}')
#     option = sys.argv[1]
    
#     if option == 'deploy':
#         deploy_ado_cli()
#     elif option == 'execute':
#         execute_ado_cli()