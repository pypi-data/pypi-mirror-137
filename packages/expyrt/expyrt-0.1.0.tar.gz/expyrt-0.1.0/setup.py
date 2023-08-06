from setuptools import setup, find_packages

setup(
    name="expyrt",
    version="0.1.0",
    description="A package for studying data science.",
    packages=find_packages(include=["expyrt", "expyrt.*"]),
)
