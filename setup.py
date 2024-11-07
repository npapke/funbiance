from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="funbiance",
    author="Norbert Papke",
    author_email="npapke@acm.org",
    description="Light ambiance using monitors and Philips Hue",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.9',
)
