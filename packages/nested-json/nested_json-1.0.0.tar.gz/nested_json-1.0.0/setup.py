import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nested_json",
    version="1.0.0",
    author="Laszlo Szikszai",
    author_email="sziklaszlo@gmail.com",
    description="A library to manage JSONs with encoded JSON more effectively (e.g. AWS Event Bridge Events, AWS API Gateway Events)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szikszail/nested-json",
    project_urls={
        "Bug Tracker": "https://github.com/szikszail/nested-json/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=["nested_json"],
    python_requires=">=3.6",
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    install_requires=[]
)
