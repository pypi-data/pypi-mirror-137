try:
    from gevault.lib.vault import Vault
except ModuleNotFoundError:
    from lib.vault import Vault

class Users(Vault):

    def __init__(self, config_file=None, server_name="default", silent=True):
        Vault.__init__(self, config_file=config_file, server_name=server_name, silent=silent)

    def create_user_token(self, user=None):
        if not user:
            raise Exception("User Name not included in function call.")
        response = self.vault.auth.token.create(role_name=self.token_role, meta={"User": user}, display_name=user)
        token = response['auth']['client_token']

        self._print_box("New Token: %s" % token)
        # Config
        config = self.read_config()
        user_tokens = config.get("admin", {}).get("userTokens", {})
        current_user_tokens = user_tokens.get(user, [])
        current_user_tokens.append(token)
        user_tokens[user] = current_user_tokens
        self.update_config("admin", {"userTokens": user_tokens})
        return token

    def list_users(self, user=None):
        accessor_ids = self.vault.auth.token.list_accessors()['data']['keys']
        accessors = [y for y in [self.vault.auth.token.lookup_accessor(x)['data'] for x in accessor_ids] if y["meta"]]
        accessor_users = [x.get("meta", {}).get("User", None) for x in accessors if x.get("meta").get("User", None)]
        self._whisper(accessor_users)
        return accessor_users

    def revoke_user_tokens(self, user=None):
        if not user:
            raise Exception("User Name not included in function call.")
        accessor_ids = self.vault.auth.token.list_accessors()['data']['keys']
        accessors = [y for y in [self.vault.auth.token.lookup_accessor(x)['data'] for x in accessor_ids] if y["meta"]]
        revoke_accessors = [x for x in accessors if x["meta"].get("User", None) == user]
        for accessor in revoke_accessors:
            self.vault.auth.token.revoke_accessor(accessor["accessor"])
        self._whisper("Deleted %i tokens" % len(revoke_accessors))

        # Config
        config = self.read_config()
        user_tokens = config.get("admin", {}).get("userTokens", {})
        try:
            del user_tokens[user]
        except KeyError:
            pass
        self.update_config("admin", {"userTokens": user_tokens})
        
    def nuke_user_tokens(self, user=None):

        accessor_ids = self.vault.auth.token.list_accessors()['data']['keys']
        accessors = [y for y in [self.vault.auth.token.lookup_accessor(x)['data'] for x in accessor_ids] if 'root' not in y['policies']]
        for accessor in accessors:
            self.vault.auth.token.revoke_accessor(accessor["accessor"])
        self._whisper("Deleted %i tokens" % len(accessors))
        self.update_config("admin", {"userTokens": {}})
