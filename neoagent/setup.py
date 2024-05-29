# setup.py

from setuptools import setup, find_packages

setup(
    name="neoagent",
    version="0.1.0",
    description="A package for Neo4j data ingestion using an AI agent.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_experimental",
        "langchain_openai",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
