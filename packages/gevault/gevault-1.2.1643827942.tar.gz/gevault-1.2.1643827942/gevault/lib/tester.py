from os.path import expanduser
from os import system
import boto3

try:
    from gevault.lib.vault import Vault
    from gevault.lib.tester_stack.stack import Stack
except ModuleNotFoundError:
    from lib.vault import Vault
    from lib.tester_stack.stack import Stack

DEFAULT_STACK_NAME = "GEVault-Test-Server"

class Test(Vault):

    def __init__(self, config_file=None, server_name="default", silent=True):
        Vault.__init__(self, config_file=config_file, server_name=server_name, silent=silent)
        profile_name = self.__get_profile_name()
        self.session = boto3.Session(profile_name=profile_name)
        self.stack = Stack(
            stack_name=self.__get_stack_name(),
            boto_session=self.session
        )

    def push_stack(self):

        (subnet_id, vpc_id) = self.__get_subnet_info()
        public_key = self.__get_public_key()

        parameters = {
            "PublicKey": public_key,
            "VpcId": vpc_id,
            "SubnetId": subnet_id
        }
        self.stack.set_parameters(parameters)
        self.stack.push(stack_type="user_data")

    def push_nat_stack(self):

        (subnet_id, vpc_id) = self.__get_subnet_info()
        ami_id = input("AWS AMI ID: ")

        parameters = {
            "AmiId": ami_id,
            "VpcId": vpc_id,
            "SubnetId": subnet_id
        }
        self.stack.set_parameters(parameters)
        self.stack.push(stack_type="nat")

    def connect(self):
        outputs = self.stack.get_outputs()
        try:
            ip_address = outputs["VaultTestPrivateIP"]
        except KeyError:
            raise Exception("IP Address of Server could not be found in stack.  Make sure to `push_stack` before connecting.")
        key_name = self._get_key_name()
        ssh_loc = expanduser("~/.ssh")
        command = "ssh ec2-user@%s -i %s/%s" % (ip_address, ssh_loc, key_name)
        self._whisper("Running command: %s" % command)
        system(command)

    def connect_nat(self):
        outputs = self.stack.get_outputs()
        try:
            ip_address = outputs["VaultTestPrivateIP"]
        except KeyError:
            raise Exception("IP Address of Server could not be found in stack.  Make sure to `push_stack` before connecting.")
        key_name = self._get_key_name()
        ssh_loc = expanduser("~/.ssh")
        command = "ssh gecloud@%s -i %s/%s" % (ip_address, ssh_loc, key_name)
        self._whisper("Running command: %s" % command)
        system(command)        

    def __get_stack_name(self):
        if not self.config.get("testStack", {}).get("stackName", None):
            stack_name = input("Stack Name (default: %s): " % DEFAULT_STACK_NAME)
            if not stack_name:
                stack_name = DEFAULT_STACK_NAME
            self.update_config("testStack", {"stackName": stack_name})
        else:
            stack_name = self.config["testStack"]["stackName"]
        return stack_name

    def __get_profile_name(self):
        if not self.config.get("testStack", {}).get("profileName", None):
            profile_name = input("AWS Profile Name: ")
            self.update_config("testStack", {"profileName": profile_name})
            return profile_name
        else:
            return self.config["testStack"]["profileName"]

    def __get_subnet_info(self):
        if not self.config.get("testStack", {}).get("subnetId", None):
            subnet_id = input("AWS SubnetId: ")
        else:
            subnet_id = self.config["testStack"]["subnetId"]
        vpc_id = self.__get_vpc_id(subnet_id)
        self.update_config("testStack", {"subnetId": subnet_id})
        return (subnet_id, vpc_id)

    def __get_vpc_id(self, subnet_id):
        response = self.session.client("ec2").describe_subnets(SubnetIds=[subnet_id])
        try:
            return response["Subnets"][0]["VpcId"]
        except IndexError:
            raise Exception("Subnet %s could not be found." % subnet_id)

    def __get_public_key(self):
        if not self.config.get("admin", {}).get("publicSigningKey", None):
            raise Exception("publicSigningKey not found in Config.  Run `gevault admin get_public_signing_key`")
        else:
            return self.config["admin"]["publicSigningKey"]
