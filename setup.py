#!/usr/bin/env python3
"""
Setup script for PDF Action Inspector
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-action-inspector",
    version="0.1.0",
    author="Foxit Software Inc.",
    author_email="support@foxitsoftware.com",
    description="A Model Context Protocol server for extracting and analyzing JavaScript Actions from PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/foxitsoftware/PDFActionInspector",
    project_urls={
        "Bug Reports": "https://github.com/foxitsoftware/PDFActionInspector/issues",
        "Source": "https://github.com/foxitsoftware/PDFActionInspector",
        "Documentation": "https://github.com/foxitsoftware/PDFActionInspector#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-action-inspector=mcp_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="pdf security analysis javascript actions mcp model-context-protocol",
    zip_safe=False,
)
