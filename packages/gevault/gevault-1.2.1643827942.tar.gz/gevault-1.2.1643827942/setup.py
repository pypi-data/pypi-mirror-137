from setuptools import setup, find_packages

setup(
    author="Barry Howard",
    author_email="barry.howard@ge.com",
    description="Python Library for communicating with vault server.",
    install_requires=['hvac', 'click'],
    keywords=['vault', 'ge', 'cloudops'],
    long_description="Python Library for communicating with GE vault server.",
    name="gevault",
    package_data={'': ['lib/tester_stack/*.yml']},
    scripts=['./gevault/gevault'],
    url="https://github.build.ge.com/Cloudpod/vault",
    version="1.2.1643827942",
    packages=find_packages(exclude=["build", "build/*"])
)
