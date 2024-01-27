from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Image-Dataset-Maker",
    version="0.1",
    description="Quickly make image datasets from image search",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ruairi OSullivan",
    author_email="ruairi.osullivan.work@gmail.com",
    url="https://github.com/Ruairi-osul/image-dataset-maker.git",
    packages=find_packages(),
    install_requires=requirements,
    keywords="computer-vision dataset image-search duckduckgo",
    python_requires=">=3.8",
)
