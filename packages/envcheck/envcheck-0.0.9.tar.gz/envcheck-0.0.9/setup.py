import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="envcheck",
    version="0.0.9",
    author="Dan Black",
    author_email="dyspop@gmail.com",
    description="A small, simple command line utility to check for, compare and merge environment variables between environment files and their .example counterparts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyspop/envcheck",
    project_urls={
        "Bug Tracker": "https://github.com/dyspop/dyspop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "envcheck=envcheck.envcheck:main",
        ]
    },
)