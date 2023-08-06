import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="termaths",
    version="0.0.4",
    author="Benoit Roux",
    author_email="b.roux3850@gmail.com",
    description="Un module de maths pour des élèves de terminales en spécialité maths ou en maths expertes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benoitrx2/termaths",
    project_urls={
        "Bug Tracker": "https://github.com/benoitrx2/termaths/issues",
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
