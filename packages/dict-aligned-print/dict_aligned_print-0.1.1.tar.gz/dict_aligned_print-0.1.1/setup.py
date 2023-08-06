import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dict_aligned_print",
    version="0.1.1",
    author="Lior Israeli",
    author_email="israelilior@gmail.com",
    description="print dict in aligned way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisrael1/dict_aligned_print",
    project_urls={
        "Bug Tracker": "https://github.com/lisrael1/dict_aligned_print/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
