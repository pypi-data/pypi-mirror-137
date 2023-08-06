import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="network-inference-mike",
    version="0.0.1",
    author="Mike Saint-Antoine",
    author_email="mikest@udel.com",
    description="Tools for gene regulatory network inference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikesaint-antoine/network_inference",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
