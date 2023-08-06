import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cleverminer",
    version="0.0.88",
    author="Petr Masa",
    author_email="code@cleverminer.org",
    description="Beyond apriori. Cleverminer is implementation of GUHA procedures that generalises apriori in many ways.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cleverminer.org",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
	"License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)