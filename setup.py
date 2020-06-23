import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smith-normal-from-corbinmcneill", # Replace with your own username
    version="0.0.1",
    author="Corbin McNeill",
    author_email="corbin.mc96@gmail.com",
    description="A tool for computing the Smith Normal Forms over arbitrary Principle Ideal Domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/corbinmcneill/snf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)

