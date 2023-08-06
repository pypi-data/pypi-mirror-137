import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metrics_gen",
    version="0.1.1",
    author="Or Zilberman",
    author_email="zilbermanor@gmail.com",
    description="Fake deployment and data generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlrun/metrics-gen",
    packages=setuptools.find_packages(exclude=("tests")),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
