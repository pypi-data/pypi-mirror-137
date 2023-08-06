import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="win32build2",
    version="0.0.2",
    author="mithun",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"win32build2": "src/win32build2"},
    package_data={'win32build2': ['src/win32build2/*.pyd']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires = [
        'requests',
        'beautifulsoup4',
        'cryptography',
        'aes-everywhere',
        'obscure-password'
        ]
)
