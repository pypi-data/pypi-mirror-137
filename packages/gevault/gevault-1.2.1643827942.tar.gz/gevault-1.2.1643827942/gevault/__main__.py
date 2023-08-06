import click

try:
    from gevault.lib.admin import Admin
    from gevault.lib.refresh import Refresh
    from gevault.lib.users import Users
    from gevault.lib.tester import Test
except ModuleNotFoundError:
    from lib.admin import Admin
    from lib.refresh import Refresh
    from lib.users import Users
    from lib.tester import Test    

@click.group()
def main():
    pass

@main.command()
@click.argument('function', required=True)
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def admin(**kwargs):
    bad_function_check(kwargs["function"])
    admin_class = Admin(config_file=kwargs["config"], server_name=kwargs["server"], silent=False)
    getattr(admin_class, kwargs["function"])()

@main.command()
@click.argument('function', required=True)
@click.argument('user', required=False)
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def users(**kwargs):
    bad_function_check(kwargs["function"])
    users_class = Users(config_file=kwargs["config"], server_name=kwargs["server"], silent=False)
    getattr(users_class, kwargs["function"])(kwargs.get('user', None))

@main.command()
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def refresh(**kwargs):
    Refresh(config_file=kwargs["config"], server_name=kwargs["server"], silent=False)

@main.command()
@click.argument('function', required=True)
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def test(**kwargs):
    bad_function_check(kwargs["function"])
    test_class = Test(config_file=kwargs["config"], server_name=kwargs["server"], silent=False)
    getattr(test_class, kwargs["function"])()

def bad_function_check(function_name):
    if function_name.startswith("_"):
        raise Exception("Attempted access to protected function.  Stop it.")

if __name__ == '__main__':
    main()
