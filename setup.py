from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name="synko",
    version="0.0.1",
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
        "License :: OSI Approved :: GPL-3.0 License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    entry_points="""
        [console_scripts]
        synko=synko.main:main
    """,
)
