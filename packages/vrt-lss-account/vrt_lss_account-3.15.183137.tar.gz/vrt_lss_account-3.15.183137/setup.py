# coding: utf-8

"""
    Veeroute.Account

    Veeroute Account Panel  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "vrt_lss_account"
VERSION = "3.15.183137"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.25.3", "six >= 1.10", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Veeroute.Account",
    author="Veeroute Support Team",
    author_email="support@veeroute.com",
    url="https://docs.veeroute.com/#/lss/account",
    keywords=["OpenAPI", "OpenAPI-Generator", "Veeroute.Account"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    Veeroute Account Panel  # noqa: E501
    """
)
