from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docums-charts-plugin",
    version="0.0.6",
    description="Docums plugin to add charts from data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="docums plugin",
    url="https://github.com/khanhduy1407/docums-charts-plugin",
    author="NKDuy",
    author_email="kn145660@gmail.com",
    license="MIT",
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["docyms>=1.1.0", "pymdown-extensions>=9.1"],
    packages=find_packages(),
    entry_points={
        "docyms.plugins": ["charts = docyms_charts_plugin.plugin:ChartsPlugin"]
    },
)
