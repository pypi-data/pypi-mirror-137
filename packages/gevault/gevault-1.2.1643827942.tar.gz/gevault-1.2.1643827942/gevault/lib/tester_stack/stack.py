#!/usr/bin/env python

"""Script for managing cloudformation stacks.
Either run script from command line with appropriate inputs or
import Stack class for running in other scripts"""

from __future__ import print_function
import random
from os.path import join, dirname, abspath
from time import sleep

from botocore.exceptions import ClientError

class Stack(object):
    """Class for creating and Managing Cloudformation Stacks"""

    def __init__(self, stack_name=None, boto_session=None, parameters=None, tags=None):

        self.stack_name = stack_name
        self.cloud_formation = boto_session.client('cloudformation')
        self.template = None

        self.set_parameters(parameters)
        self.set_tags(tags)
        self.outputs = self.get_outputs()

    def push(self, wait=True, delete=True, stack_type=None):
        """Push changes to stack.  Automatically performs creates, updates, and deletes"""
        if stack_type not in ["user_data", "nat"]:
            raise Exception("stack_type must be 'test' or 'nat'")
        if stack_type == "user_data":
            file_name = "user_data_cloudformation.yml"
        if stack_type == "nat":
            file_name = "nat_cloudformation.yml"
        with open(join(dirname(abspath(__file__)), file_name)) as cf_file:
            self.template = cf_file.read()
            cf_file.close()

        while True:
            status = self.get_status()
            if not status:
                print("No stack found.  Creating...")
                self.__create_stack()
                break
            elif "in_progress" in status:
                print("Status status is %s.  Waiting..." % status)
                sleep(10)
            elif "complete" in status:
                if status == "delete_complete":
                    print("Recreating Stack...")
                    self.__create_stack()
                    break
                elif status == "rollback_complete":
                    if not delete:
                        raise BaseException("Stack status is %s, but no delete flag found." % status)
                    print("Rollback Completed.  Deleting Stack...")
                    self.__delete_stack()
                    sleep(15)
                else:
                    print("Updating Stack...")
                    response = self.__update_stack()
                    if not response:
                        print("No stack updates.  Moving on.")
                        return
                    break
            elif "failed" in status:
                if not delete:
                    raise BaseException("Stack status is %s, but no delete flag found." % status)
                print("Failure Found.  Deleting Stack...")
                self.__delete_stack()
                sleep(15)

        while True and wait:
            status = self.get_status()
            if "rollback_complete" in status:
                raise BaseException("Stack failed to update/create. %s" % status)
            elif "complete" in status:
                print("Stack status is %s.  Moving on." % status)
                self.outputs = self.get_outputs()
                return
            elif "in_progress" in status:
                print("Status is %s.  Waiting..." % status)
                sleep(15)
            else:
                raise BaseException("Stack failure found. %s" % status)

    def __create_stack(self):
        """Creates stack"""
        return self.cloud_formation.create_stack(
            StackName=self.stack_name,
            TemplateBody=self.template,
            Parameters=self.parameters,
            Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
            Tags=self.tags
        )

    def __delete_stack(self):
        """Deletes Stack"""
        return self.cloud_formation.delete_stack(
            StackName=self.stack_name
        )

    def __update_stack(self):
        """Updates Stack"""
        try:
            return self.cloud_formation.update_stack(
                StackName=self.stack_name,
                TemplateBody=self.template,
                Parameters=self.parameters,
                Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
                Tags=self.tags
            )
        except ClientError as update_error:
            if "No updates" in update_error.response['Error']['Message']:
                return None
            raise update_error

    # Parameters
    def set_parameters(self, input_parameters):
        """Set parameters attribute according to required Stack format"""
        parameters = []
        if input_parameters:
            for key, value in input_parameters.items():
                parameters.append(self.__return_parameter(key, value))
        self.parameters = parameters

    @staticmethod
    def __return_parameter(key, value):
        if isinstance(value, list):
            return {
                "ParameterKey": str(key),
                "ParameterValue": ",".join(value)
            }
        return {
            "ParameterKey": str(key),
            "ParameterValue": str(value)
        }

    # Tags
    def set_tags(self, input_tags):
        """Set tags attribute according to required Stack format"""
        tags = []
        if input_tags:
            for key, value in input_tags.items():
                tags.append(self.__return_tag(key, value))
        self.tags = tags

    @staticmethod
    def __return_tag(key, value):
        return {
            "Key": key,
            "Value": value
        }

    def get_outputs(self):
        """Returns outputs of Stack"""
        try:
            response = self.exponential_backoff(
                self.cloud_formation.describe_stacks,
                {"StackName": self.stack_name}
            )
        except ClientError as describe_error:
            if describe_error.response['Error']['Code'] == 'ValidationError':
                return None
            else:
                raise describe_error
        output_list = response['Stacks'][0].get('Outputs', [])
        self.outputs = {x["OutputKey"]: x["OutputValue"] for x in output_list}
        return self.outputs

    @staticmethod
    def exponential_backoff(func, args):
        """
        Perform exponential backoff on a function call
        :param func: Function
        :param dict args: Arguments
        :return: Function results
        """
        backoff_count = 0
        max_backoff_times = 10
        base_delay = 0.1
        delay = base_delay + random.uniform(0, 1)

        while True:
            try:
                return func(**args)
            except ClientError as e:
                if e.response['Error']['Code'] == 'Throttling':
                    pass
                else:
                    raise

                if backoff_count < max_backoff_times:
                    print('delay = %f, backoff_count = %s, args = %s, error_code = %s)' % (
                        delay, backoff_count, args, e.response['Error']['Code']
                    ))
                    sleep(delay)
                    backoff_count += 1
                    delay = base_delay * pow(2, backoff_count) + random.uniform(0, 1)
                else:
                    raise

    def get_status(self):
        """Returns status of Stack"""
        try:
            response = self.exponential_backoff(
                self.cloud_formation.describe_stacks,
                {"StackName": self.stack_name}
            )
            
        except ClientError as describe_error:
            if describe_error.response['Error']['Code'] == 'ValidationError':
                return None
            else:
                raise describe_error
        return response['Stacks'][0]['StackStatus'].lower()

    def update_termination_protection(self, enabled):
        """Enable or disable termination protection"""
        self.cloud_formation.update_termination_protection(
            EnableTerminationProtection=enabled,
            StackName=self.stack_name
        )
