# setup.py

from setuptools import setup, find_packages
with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="neo-pusher",
    version="1.0.0",
    description="A package for Neo4j data ingestion using an AI agent.",
    author="Siddharth Choudhury",
    author_email="siddharthc@mindfiresolutions.com",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
    install_requires=[
        "langchain",
        "langchain_experimental",
        "langchain_openai",
        "pandas",
        "neo4j"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
