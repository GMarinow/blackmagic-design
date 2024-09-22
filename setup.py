from setuptools import setup, find_packages

setup(
    name="blackmagic-design",
    version="0.1.0",
    author="Georgi Marinov",
    author_email="georgi.marinow@gmail.com",
    description="Blackmagic Design API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GMarinow/blackmagic-design",
    project_urls = {
        "Documentation": "https://github.com/GMarinow/blackmagic-design/blob/main/README.md",
        "Source": "https://github.com/GMarinow/blackmagic-design"
    },
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities"
    ],
    python_requires='>=3.10, <=3.12',
)
