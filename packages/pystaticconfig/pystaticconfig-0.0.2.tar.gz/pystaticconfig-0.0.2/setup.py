import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pystaticconfig",
    version="0.0.2",
    author="Ivan Chistiakov",
    description="JSON config with static class in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IvanFoke/PyStaticConfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# python setup.py sdist bdist_wheel
