import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-pv-lib",
    version="1.2202.2",
    author="my-PV GmbH",
    author_email="info@my-pv.com",
    description="my-PV python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.my-pv.com/de/info/downloads",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)