import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="explicit_numpy_broadcast",
    version="1.0.2",
    author="bellecp",
    author_email="pierre.bellec@rutgers.edu",
    description="Explicit broadcasting rules in Jupyter for numpy arrays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellecp/explicit_numpy_broadcast",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
