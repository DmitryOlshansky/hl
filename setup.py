import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hl",
    version="0.2.0a",
    author="Dmitry Olshansky",
    author_email="dmitry@olshansky.me",
    description="HL - Host List, a simple flexible fuzzy search/execute tool for lists of hosts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/example-project",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'hl=hl.hl_cli:main_entry',
            'hl-db=hl.hl_cli:db_entry'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)