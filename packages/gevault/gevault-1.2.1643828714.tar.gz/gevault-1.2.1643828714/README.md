# Gevault

The gevault pypi package is designed to help managed vault servers, specifically those hosted by the GE Cloud DevOps Team.  By helping to intialize the server, store secrets, create users, and refresh user tokens, the library should provide all the functionality needed to support a server -- serverless or otherwise -- without having to manually look up and construct curl commands.  The locally stored config file will also automatically be updated to reflect new credentials to be used in future calls.

## Setup

The pypi package can be install with the following command:

```bash
sudo pip3 install -I gevault
```

Afterwards, it can be run from either the command line or imported to python3 scripts as shown:

```bash
gevault refresh
```

OR

```python
import gevault
```

## Proxy

Currently the DevOps and Manged vault servers are deployed at using the domain name: cloudpod.apps.ge.com which requires being on proxy to reach.  However, I have personally not been able to this these endpoints without disabling proxy variables, so I've included a bash script I use to setup my proxy for hitting the endpoint that I call from my .bashrc file.  Your results may vary.

```bash
function vault_on {
  sudo pkill -f /Applications/MyAppsAnywhere.app
  open /Applications/BIG-IP\ Edge\ Client.app
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY EC2_JVM_ARGS
  networksetup -setautoproxystate "Wi-Fi" off
  networksetup -setautoproxyurl "Wi-Fi" "http://corp.setpac.ge.com/pac.pac"
}
```

## Commands

The gevault package can be run from either the command line or the as an import to a python3 script.  The following two options can be specified at the command line or be given as inputs to the subclasses specified in the next section.

* config: The relative path of the config file to be generated and read by the package.  The default location for this is in the user's ssh folder.

* server:  The name of the server you wish to access/manage.  If none is specified a "default" server key will be created in the config file.  You may, however, choose to give the server a name with this option to differentiate it from other servers that require different secrets, etc.

## Public Functions

The functions are split into three subcategories:

- Admin:  For initializing new vault clusters and unsealing new vault servers.
- Users:  For managing User Tokens by Admins.
- Refresh:  For refreshing vault ssh keys.

### Admin

* **initialize** -- Initialize a new vault server cluster, i.e. there is no existing backend.  This will run a series of commands on the server to set it up as well as storing tokens, unseal keys, and a public ssh signing key inside your config file.  For a full list of stuff going on, check out the [vault server github.](https://github.build.ge.com/cloudpod/vault)  A new server does not require authentication until it is initialized.

```bash
gevault admin initialize --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Admin(server="cloudpod", config="~/.ssh/vault-config.json").initialize()
```

* **unseal** - Unseal a vault server.  Vault servers needs to be unsealed so that it can decrypt an already existing backend.  This will be done automatically upon initialization, but must be done again when a new server is created.  This will require the unseal keys to already exist in the config file.

```bash
gevault admin unseal --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Admin(server="cloudpod", config="~/.ssh/vault-config.json").unseal()
```

* **get_public_signing_key** - Get he public signing key from the vault server.  The public signing key needs to be given to new servers that users access with vault tokens, so this function will retrieve it and print it out.

```bash
gevault admin get_public_signing_key --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Admin(server="cloudpod", config="~/.ssh/vault-config.json").get_public_signing_key()
```

* **write_signing_key** - Write the signing key to the server.  This helps to generate our own ssh keys so that they can be reused in case the server needs to be regenerated without having to update the ami.  Takes the values stored inside the config file.  If none exist, `ssh keygen` is run on the users machine and the result is used.

```bash
gevault admin write_signing_key --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Admin(server="cloudpod", config="~/.ssh/vault-config.json").write_signing_key()
```

* **delete_signing_key** - Delete the signing key from the server -- presumably to replace it with another one.  This operation must be run before write_signing_key if a signing key already exists on the server.

```bash
gevault admin delete_signing_key --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Admin(server="cloudpod", config="~/.ssh/vault-config.json").delete_signing_key()
```


### Users

* **create_user_token** - Create a user token for the specified username -- SSO is recommended.  The token will be printed out as well as added to the config file.  This function requires a root/master token.

```bash
gevault users create_user_token 212000000 --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Users(server="cloudpod", config="~/.ssh/vault-config.json").create_user_token("212000000")
```

* **list_users** - Lists all users that have vault tokens assigned to them.  This function requires a root/master token.

```bash
gevault users list_users --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Users(server="cloudpod", config="~/.ssh/vault-config.json").list_users()
```

* **revoke_user_tokens** - Revoke all vault tokens associated with a specific user.  This function requires a root/master token.

```bash
gevault users revoke_user_tokens 212000000 --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Users(server="cloudpod", config="~/.ssh/vault-config.json").revoke_user_tokens("212000000")
```

### Refresh

Refresh a vault ssh key with a vault token

```bash
gevault refresh --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Refresh(server="cloudpod", config="~/.ssh/vault-config.json")
```

### Test

* **push_stack** - Create/Update a cloudformation stack with an EC2 instance and supporting resources.  The user data for the EC2 instance takes in the public key as parameter so that you can test authentication.  AWS credentials are required.

```bash
gevault test push_stack --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Test(server="cloudpod", config="~/.ssh/vault-config.json").push_stack()
```

* **connect** - SSH to the instance in the cloudformation stack by generating an SSH command for the ip address and vault key.  Successful connection indicates a working vault server and user token.  A refreshed token and AWS credentials are required.

```bash
gevault test connect --server cloudpod --config ~/.ssh/vault-config.json
```

```python
gevault.Test(server="cloudpod", config="~/.ssh/vault-config.json").connect()
```