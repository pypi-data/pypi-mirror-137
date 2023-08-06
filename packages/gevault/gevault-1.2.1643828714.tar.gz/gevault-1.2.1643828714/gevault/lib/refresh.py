from os import environ
from os.path import isfile, join
from os.path import expanduser
import json
import requests

from requests.exceptions import ReadTimeout



try:
    from gevault.lib.vault import Vault
    from gevault.lib.admin import MOUNT_POINT, SIGNING_ROLE
except ModuleNotFoundError:
    from lib.vault import Vault
    from lib.admin import MOUNT_POINT, SIGNING_ROLE

DEFAULT_VAULT_VARIABLE = "VAULT_TOKEN"

class Refresh(Vault):

    def __init__(self, config_file=None, server_name="default", silent=True):
        Vault.__init__(self, config_file=config_file, server_name=server_name, silent=silent)
        self.ssh_loc = expanduser("~/.ssh")
        self.key_name = self._get_key_name()
        self.pubkey_path = "%s/%s.pub" % (self.ssh_loc, self.key_name)
        self.refresh_token = self.__get_refresh_token()

        self.gen_ssh_key()
        cert = self.request_certificate()
        self.create_cert_file(cert)

    def gen_ssh_key(self):
        self._whisper("Generating Key Pair...")
        if isfile(self.pubkey_path): ## keypair exists but is stale
            self._command("echo -e 'y' | ssh-keygen -q -t rsa -b 4096  -N '' -f %s/%s 2>/dev/null <<< y >/dev/null" % (self.ssh_loc, self.key_name))

        else: ## keypair does not exist
            self._command("echo -e 'y' | ssh-keygen -q -t rsa -b 4096 -f %s/%s -N ''" % (self.ssh_loc, self.key_name))

    def request_certificate(self):
        with open(self.pubkey_path, 'r') as pubkey:
            key = pubkey.read().replace('\n', '')

        body = {
            "valid_principals": "ubuntu,ec2-user,gecloud,cops,centos",
            "public_key": key,
            "extension":{"permit-pty": ""}
        }

        req_sess = requests.Session()
        req_sess.trust_env = False

        signing_role = self.config.get("user", {}).get("signingRole", SIGNING_ROLE)
        url = f"{self._get_url()}/v1/{MOUNT_POINT}/sign/{signing_role}"
        headers = {'X-Vault-Token': self.refresh_token}

        self._whisper("Requesting Signature...")
        response = req_sess.post(url, headers=headers, data=json.dumps(body), timeout=4)
        response.raise_for_status
        response_dict = json.loads(response.text)
        if response_dict.get("errors", None):
            raise Exception(response_dict["errors"])

        return json.loads(response.text)['data']['signed_key']


    def create_cert_file(self, cert):
        self._whisper("Writing Vault Key...")
        with open(join(self.ssh_loc, "%s-cert.pub" % self.key_name), 'w') as cert_file:
            cert_file.write(cert)

    def __get_refresh_token(self):
        # Config Token
        if self.config.get("user", {}).get("refreshToken", None):
            self._whisper("Token found in config file.")
            return self.config["user"]["refreshToken"]

        # Config Variable
        variable = self.config.get("user", {}).get("refreshTokenVariable", None)
        try:
            token = environ[variable]
            self._whisper("Token found in environment variable %s." % variable)
            return token
        except KeyError:
            self._whisper("Token NOT found in environment variable %s." % variable)
        except TypeError:
            pass

        # Default Variable
        try:
            token = environ[DEFAULT_VAULT_VARIABLE]
            self._whisper("Token found in environment variable %s." % DEFAULT_VAULT_VARIABLE)
            self.update_config("user", {"refreshTokenVariable": DEFAULT_VAULT_VARIABLE})
            return token
        except KeyError:
            pass

        # Input Variable
        new_variable = input("Vault Token Variable Name: ")
        self.update_config("user", {"refreshTokenVariable": new_variable})
        try:
            token = environ[new_variable]
            self._whisper("Token found in environment variable %s." % new_variable)
            return token
        except KeyError:
            raise Exception("Variable: %s could not be found in environment" % new_variable)
