from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='timetracker-cli2',
    version='0.1.1',
    author="Bruno Garrofe",
    author_email="bruno.garrofe@gmail.com",
    description="A command line interface for the BairesDev TimeTracker API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.*",
    py_modules=['timetracker'],
    install_requires=[
        'click>=8.0.*',
        'requests>=2.27.*',
        'rich>=11.1.*',
        'dateparser>=1.1.*'
    ],
    entry_points={
        'console_scripts': [
            'timetracker = timetracker.cli:cli',
        ],
    },
)
