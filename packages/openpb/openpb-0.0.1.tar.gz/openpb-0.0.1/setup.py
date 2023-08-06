import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="openpb",
    version="0.0.1",
    author="Nicolas Posocco",
    author_email="nicolas.posocco@gmail.com",
    description="A package for efficient problem solving",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nposocco/openpb",
    project_urls={
        "Bug Tracker": "https://github.com/nposocco/openpb/issues",
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
