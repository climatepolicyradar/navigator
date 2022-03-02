"""Setup navigator common python package"""


from setuptools import setup, find_packages

setup(
    name="navigator",
    version="0.0.1",
    author="Chris Ballard",
    packages=find_packages(),
    install_requires=["boto3"],
)
