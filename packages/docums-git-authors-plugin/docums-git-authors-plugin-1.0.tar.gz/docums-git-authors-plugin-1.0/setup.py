from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docums-git-authors-plugin",
    version="1.0",
    description="docums plugin to display git authors of a page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="docums git contributors committers authors plugin",
    url="https://github.com/khanhduy1407/docums-git-authors-plugin",
    author="NKDuy",
    author_email="kn145660@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    install_requires=["docums>=1.0.0.0"],
    packages=find_packages(),
    entry_points={
        "docums.plugins": [
            "git-authors = docums_git_authors_plugin.plugin:GitAuthorsPlugin"
        ]
    },
)
