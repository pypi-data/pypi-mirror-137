import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="walax",
    version="1.1.5",
    author="Matt Barry",
    author_email="matt@hazelmollusk.org",
    description="Walax Django API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hazelmollusk/django-walax",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
