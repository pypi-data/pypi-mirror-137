import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lieGenTools",
    version="0.1.0",
    author="SoftLab",
    author_email="",
    description="A Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # List all your dependencies inside the list
    install_requires=['antlr4-python3-runtime'],
    license='MIT'
)
