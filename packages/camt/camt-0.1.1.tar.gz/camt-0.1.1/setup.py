from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='camt',
    version='0.1.1',
    author='Lucien Makutano',
    author_email='makutanolucien@gmail.com',
    url='https://amt.africa',
    description='Zip labeled images',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'camt = camt.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='amt africa camt compression python package camt',
    install_requires=requirements,
    zip_safe=False
)
