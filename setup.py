from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements=f.read().splitlines()
    
setup(
    name="multi-ai",
    version="0.1",
    author="Kumar",
    packages=find_packages(),
    install_requires=requirements
)
