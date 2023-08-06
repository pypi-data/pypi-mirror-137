import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PACKAGE_NAME= "Demo-pkg"
USER_NAME ="sarikamohan08"
PROJECT_NAME="Demo_pkg"

setuptools.setup(
    name=f"{PACKAGE_NAME}-{USER_NAME}",
    version="0.0.2",
    author=USER_NAME,
    author_email="sarikamohan08@gmail.com",
    description="A small demo package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PACKAGE_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PACKAGE_NAME}/issues",
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
        "numpy==1.21.5",
        "pandas==1.1.5",
        "joblib==1.1.0"
    ]
)