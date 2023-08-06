import json
from os.path import expanduser

from hvac.exceptions import InvalidRequest
try:
    from gevault.lib.vault import Vault
except ModuleNotFoundError:
    from lib.vault import Vault

MOUNT_POINT = 'ssh-client-signer'
SIGNING_ROLE = "vault-signing-role"

SHARES = 5
THRESHOLD = 3

class Admin(Vault):

    def __init__(self, config_file=None, server_name="default", silent=True):
        Vault.__init__(self, config_file=config_file, server_name=server_name, silent=silent)

    def initialize(self):
        """
        To be performed when a new vault cluster is being created.
        This does not apply to simply creating a new server.
        This will create new keys and will mean having to relaunch instances
        using vault creds.  Don't do this on redeploy!
        """
        if self.config:
            text = ""
            while text.lower() not in ["y", "n"]:
                text = input("Server already exists in config.  Some values may be overwritten.  Continue? (y/n)")
    
            if text.lower() == "n":
                self._whisper("Exiting...")
                return

        if self.status_check() == 501:
            self._whisper("Status 501:  Initializing Vault...")
            response = self.vault.sys.initialize(SHARES, THRESHOLD)

            self.vault.token = response['root_token']
            self.update_config("admin", {
                "rootToken": response['root_token'],
                "unsealKeys": response['keys']
            })
            self._whisper("Vault Initialized.")
    
        # -------------------------------

        if self.status_check() == 503:
            self._whisper("Status 503:  Unsealing Vault...")
            self.unseal()

        # -------------------------------

        if self.status_check() == 200:
            self._whisper("Status 200:  Running Setup...")
            self.set_vault()
            self.__mount_ssh_backend()
            self.write_signing_key()
            self.__create_signing_role()
            self.__create_token_role()

        if not self.config["admin"].get("masterToken", None):
            self.update_config("admin", {"masterToken": self.__create_master_token()})

    def __mount_ssh_backend(self):
        self._whisper('Mounting SSH backend...')
        try:
            self.vault.sys.enable_secrets_engine('ssh', path=MOUNT_POINT)
        except InvalidRequest:
            self._whisper("SSH backend already mounted...")


    # --- SSH Keys ---

    def write_signing_key(self, public_key=None, private_key=None):
        signing_key_address = "%s/config/ca" % MOUNT_POINT
        try:
            public_key = self.config["admin"]["publicSigningKey"]
        except:
            public_key = None
        try:
            private_key = self.config["admin"]["privateSigningKey"]
        except:
            private_key = None
    
        try:
            if not public_key and not private_key:
                key_dict = self.__generate_signing_key()
                public_key = key_dict["public_key"]
                private_key = key_dict["private_key"]
            elif public_key and private_key:
                pass
            else:
                raise Exception("Public AND Private Keys must either both exist or neither.")
            self.vault.write(signing_key_address, public_key=public_key, private_key=private_key)
            self.update_config("admin", {
                "publicSigningKey": public_key,
                "privateSigningKey": private_key
            })
        except InvalidRequest as error:
            if "keys are already configured" in error:
                self._whisper("Signing Key already written...")
            else:
                raise
            

    def delete_signing_key(self):
        signing_key_address = "%s/config/ca" % MOUNT_POINT
        self.vault.delete(signing_key_address)

    def __generate_signing_key(self):
        ssh_loc = expanduser("~/.ssh")
        key_name = "vault-signing-%s" % self.server_name
        self._command("echo -e 'y' | ssh-keygen -q -t rsa -b 4096 -f %s/%s -N ''" % (ssh_loc, key_name))
        with open("%s/%s.pub" % (ssh_loc, key_name), 'r') as public_file:
            public_key = public_file.read().replace('\n', '')
            public_file.close()
        with open("%s/%s" % (ssh_loc, key_name), 'r') as private_file:
            private_key = private_file.read()
            private_file.close()
        return {
            "public_key": public_key,
            "private_key": private_key
        }
        

    def get_public_signing_key(self):
        signing_key_address = "%s/config/ca" % MOUNT_POINT
        key = self.vault.read(signing_key_address)['data']['public_key'].replace("\n", "")
        self.update_config("admin", {"publicSigningKey": key})
        self._whisper(key)
        return key


    # --- SSH ROLES ---

    def __create_signing_role(self):
        try:
            self.vault.write(
                '%s/roles/%s' % (MOUNT_POINT, SIGNING_ROLE),
                allow_user_certificates=True,
                allowed_users="*",
                key_type="ca",
                ttl="30m0s",
                default_extensions=[{ "permit-pty": "" }]
            )
        except InvalidRequest:
            self._whisper("Signing Role already created...")

    def __create_token_role(self):
        policy = {
            "path": {
                "%s/sign/*" % MOUNT_POINT: {
                    "capabilities": [
                        "read",
                        "create",
                        "update",
                        "list"
                    ]
                }
            }
        }
        self.vault.sys.create_or_update_policy(self.token_role, json.dumps(policy))
        return self.vault.auth.token.create_or_update_role(self.token_role, allowed_policies=self.token_role, renewable=True)
        # return self.vault.create_token_role(self.token_role, allowed_policies=self.token_role, period='87600h')

    def __create_master_token(self):
        return self.vault.auth.token.create(policies=['root'], ttl='87600h')['auth']['client_token']

    def __get_policy(self):
        return self.vault.sys.read_policy(name=self.token_role)

    # --- Unseal ---

    def unseal(self):
        self._whisper("Unsealing Vault...")
        vault_keys = self._get_unseal_keys()
        self.vault.sys.submit_unseal_key(vault_keys[0])
        self.vault.sys.submit_unseal_key(vault_keys[1])
        self.vault.sys.submit_unseal_key(vault_keys[2])
        self._whisper("Unseal Keys Submitted.")
