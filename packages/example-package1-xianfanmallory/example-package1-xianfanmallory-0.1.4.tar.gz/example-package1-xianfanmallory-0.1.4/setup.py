import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-package1-xianfanmallory",
    version="0.1.4",
    author="Xian Fan Mallory",
    author_email="xfan2@fsu.edu",
    description="Simulating single cell sequencing data",
    long_description=long_description,
    url="https://github.com/compbiofan/SimSCSnTree",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "anytree",
        "graphviz",
    ],
)
