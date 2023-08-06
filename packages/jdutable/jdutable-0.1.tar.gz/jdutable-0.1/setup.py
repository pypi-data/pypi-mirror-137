import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jdutable",
    version="0.1",
    scripts=["bin/jdutable"],
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A simple table-data visualizer for command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeandemeusy/jdu-table",
    packages=["jdutable"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy"],
)
