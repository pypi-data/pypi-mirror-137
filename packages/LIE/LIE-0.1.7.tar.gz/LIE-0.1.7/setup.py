import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LIE",
    version="0.1.7",
    author="SoftLab",
    author_email="",
    description="A LIE++ to python compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # List all your dependencies inside the list
    install_requires=['antlr4-python3-runtime', 'lieGenTools', 'argparse'],
    license='MIT'
)
