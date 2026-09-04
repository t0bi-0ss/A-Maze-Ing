from setuptools import setup, find_packages

# python3 setup.py bdist_wheel
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="maze_generator",
    version="1.0.0",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
