import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpoems",
    version="1.0.2",
    author="Neeraj Mula",
    author_email="neeraj.mula@rutgers.edu",
    description="Generate poems with comments from Reddit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Acryptarch/Reddit-Poem-Generator",
    packages=['rpoems'],
    install_requires=['pronouncing', 'psaw'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)