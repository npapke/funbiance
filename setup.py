from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="funbiance",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.9',
)
