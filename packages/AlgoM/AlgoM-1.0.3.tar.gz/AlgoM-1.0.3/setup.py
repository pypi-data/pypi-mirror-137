import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AlgoM", # Replace with your own username
    version="1.0.3",
    author="Marta Religa",
    author_email="marta.religa@hotmail.com",
    description="Python algorithms and data structures library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martarel/AlgoPack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)