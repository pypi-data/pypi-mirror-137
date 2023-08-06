from setuptools import setup, find_packages

setup(
    name="aiandml",
    version="1.0.6",
    description=""" The description of the package   """,
    long_description_content_type="text/markdown",
    long_description=open('README.txt').read(),
    # url="https://github.com/ashleshmd/aiandml",
    author="Ashlesh M D",
    author_email='ashleshmd@gmail.com',
    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.8",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 ],
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)