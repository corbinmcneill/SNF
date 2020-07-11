import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smithnormalform",
    version="0.5.0",
    author="Corbin McNeill",
    author_email="corbin.mc96@gmail.com",
    description=("A tool for computing the Smith Normal Forms " +
                 "over arbitrary Principle Ideal Domains"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/corbinmcneill/snf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics"],

    python_requires='>=3.6'
)
