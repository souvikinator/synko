from setuptools import setup, find_packages
from synko.constants import APP_NAME, APP_VERISON

print(f">>> {APP_NAME}, VERISON {APP_VERISON}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name=APP_NAME,
    version=APP_VERISON,
    author="souvikinator",
    author_email="souvikat001@gmail.com",
    license="GPL-3.0",
    description="Sync application configurations and settings across multiple multiplatform devices. Currently supports linux and osx, working in progress for windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/souvikinator/synko",
    keyword="cli, sync, config, settings, application, configuration, linux, osx",
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    entry_points="""
        [console_scripts]
        synko=synko.main:main
    """,
)
