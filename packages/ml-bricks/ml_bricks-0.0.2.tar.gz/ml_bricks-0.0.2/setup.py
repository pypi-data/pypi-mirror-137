# https://medium.com/@udiyosovzon/things-you-should-know-when-developing-python-package-5fefc1ea3606
import setuptools
with open('./requirements.txt') as f:
    required = f.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="ml_bricks",
    version="0.0.2",
    author="Jerin KA",
    author_email="me@example.com",
    description="Common utils package",
    url = 'https://github.com/user/reponame',
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)
