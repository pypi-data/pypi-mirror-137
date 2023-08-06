import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="merkletreepy",
    version="0.0.2",
    author="Callista Chang",
    author_email="changcallista@gmail.com",
    description="Python port of merkletreejs",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/callistachang/merkletreepy",
    project_urls={
        "Bug Tracker": "https://github.com/callistachang/merkletreepy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.6",
)
