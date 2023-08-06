import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udnn",
    version="0.0.3",
    author="Dimitrios Bellos",
    author_email="Dimitrios.Bellos@nottingham.ac.uk",
    description="UDNN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DimitriosBellos/UDNN",
    packages=setuptools.find_packages(),
    python_requires='>=3.6.4',
    install_requires=['numpy', 'pillow', 'pytorch>=0.4', 'h5py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
