import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="ultratimeseries-api",
    version="1.0.0",
    description="A python wrapper around the UTS REST API.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Two Impulse",
    author_email="daniel.mendonca@twoimpulse.com",
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["uts"],
    install_requires=["requests"]
)