from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='InformativeFeatureSelection',
    packages=setuptools.find_packages(),
    version='2.0.2',
    description="Package which provides an algorithm feature selection which considers class separability and an "
                "implementation of Informative Normalized Difference Index (INDI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mukhin Artem',
    author_email='artemmukhinssau@gmail.com',
    url='https://gitlab.com/rustam-industries/feature_extractor',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ], install_requires=[]
)
