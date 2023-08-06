import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="issuudl-saperoi",
    version="0.2.1",
    author="Saperoi",
    author_email="uesugi.sapero@gmail.com",
    description="A python-based individual page downloader for Issuu.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saperoi/issuudl-py",
    project_urls={
        "Bug Tracker": "https://github.com/saperoi/issuudl-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=['issuudl'],
    python_requires=">=3.6",
)