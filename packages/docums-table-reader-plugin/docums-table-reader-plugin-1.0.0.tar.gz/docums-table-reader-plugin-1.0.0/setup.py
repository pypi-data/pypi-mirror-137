from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docums-table-reader-plugin",
    version="1.0.0",
    description="Docums plugin to directly insert tables from files into markdown.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="docums plugin",
    url="https://github.com/khanhduy1407/docums-table-reader-plugin",
    author="NKDuy",
    author_email="kn145660@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["docums>=1.0.0.0", "pandas>=1.1", "tabulate>=0.8.7", "PyYAML>=5.4.1"],
    packages=find_packages(),
    entry_points={
        "docums.plugins": [
            "table-reader = docums_table_reader_plugin.plugin:TableReaderPlugin"
        ]
    },
)
