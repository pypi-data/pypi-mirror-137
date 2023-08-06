"""Setup for MQTT hass base."""
import sys

from setuptools import setup

from mqtt_hass_base.__version__ import VERSION

if sys.version_info < (3, 7):
    sys.exit("Sorry, Python < 3.7 is not supported")

install_requires = list(val.strip() for val in open("requirements.txt"))
tests_require = list(val.strip() for val in open("test_requirements.txt"))

setup(
    name="mqtt-hass-base",
    version=VERSION,
    description="Bases to build mqtt daemon compatible with Home Assistant",
    author="Thibault Cohen",
    author_email="titilambert@gmail.com",
    url="http://gitlab.com/titilambert/mqtt_hass_base",
    packages=["mqtt_hass_base", "mqtt_hass_base/entity"],
    license="Apache 2.0",
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
