import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="traducteur",
    version="0.1.0",
    author="seppedelanghe",
    author_email="seppedelanghe17@gmail.com",
    description="Traducteur is a simple database manager using pydantic models. Currently only supports mongodb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seppedelanghe/traducteur",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.1',
)