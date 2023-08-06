from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docums-enumerate-headings-plugin",
    version="0.5.0",
    description="Docums Plugin to enumerate the headings (h1-h6) across site pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="docums enumerate headings plugin",
    url="https://github.com/khanhduy1407/docums-enumerate-headings-plugin.git",
    author="NKDuy",
    author_email="kn145660@gmail.com",
    license="MIT",
    python_requires=">=3.5",
    install_requires=["docums>=1.0.0.0", "beautifulsoup4>=4.9.0"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    entry_points={
        "docums.plugins": [
            "enumerate-headings=docums_enumerate_headings_plugin.plugin:EnumerateHeadingsPlugin",
        ]
    },
)
