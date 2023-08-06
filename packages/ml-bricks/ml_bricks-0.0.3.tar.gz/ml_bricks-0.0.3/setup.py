# https://medium.com/@udiyosovzon/things-you-should-know-when-developing-python-package-5fefc1ea3606
import setuptools
with open('./requirements.txt') as f:
    required = f.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="ml_bricks",
    version="0.0.3",
    author="Jerin K A",
    author_email="jerin.electronics@gmail.com",
    description="Common utils for machine learning, computer vision",
    url = 'https://github.com/jerinka/ml_bricks',
    download_url = 'https://github.com/jerinka/ml_bricks/archive/refs/tags/v0.0.3.tar.gz',
    keywords = ['machine-learning', 'utils', 'vision-utils'],
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)
