from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="neo-pusher",  # Your package name
    # use_scm_version=True,  # Use setuptools-scm to handle versioning
    version = "1.1.3",
    # use_scm_version={"local_scheme": "no-local-version"},
    # Avoid using local versions
    setup_requires=[
        "setuptools>=42",
        "setuptools-scm",
    ],  # Use attr to get the version from your package
    description="A package for Neo4j data ingestion using an AI agent.",
    author="Mindfire Digital LLP",
    author_email="siddharthc@mindfiresolutions.com",
    packages=find_packages(
        where="."
    ),  # Specifies that packages are in the root directory
    package_dir={"": "."},  # Root directory is the package directory
    long_description=long_description,
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
    install_requires=[
        "langchain",
        "langchain_experimental",
        "langchain_openai",
        "pandas",
        "neo4j",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
