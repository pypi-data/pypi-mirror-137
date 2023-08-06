import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="BayesPermus",
    version="1.0.0",
    author="Jairo Rojas-Delgado",
    author_email="jrojasdelgado@bcamath.org",
    description="Bayesian inference of algorithm performance using permutation models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ml-opt/BayesPermus",
    project_urls={
        "Bug Tracker": "https://github.com/ml-opt/BayesPermus/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
    packages=setuptools.find_packages(where="src"),
)