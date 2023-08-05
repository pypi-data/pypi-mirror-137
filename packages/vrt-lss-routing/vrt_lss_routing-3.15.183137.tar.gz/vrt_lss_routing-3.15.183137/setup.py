# coding: utf-8

"""
    Veeroute.Routing

    Veeroute Routing API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "vrt_lss_routing"
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
    description="Veeroute.Routing",
    author="Veeroute Support Team",
    author_email="support@veeroute.com",
    url="https://docs.veeroute.com/#/lss/routing",
    keywords=["OpenAPI", "OpenAPI-Generator", "Veeroute.Routing"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    Veeroute Routing API  # noqa: E501
    """
)
