from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mallgroup_python_lib",
    version="0.0.5",
    description="Official Mallgroup Library",
    author="Data Engineering Mallgroup",
    author_email="dataengineering@mallgroup.com",
    py_modules=["mallgroup_python_lib"],
    packages=find_packages(include=['mallgroup_python_lib', 'mallgroup_python_lib.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={"dev": ["pytest"]},
)
