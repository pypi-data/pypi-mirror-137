import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Indonesia-latestearthquake",
    version="0.2",
    author="Eko S Wibowo, Gustus",
    author_email="gustussitanggang@gmail.com",
    description="Package with beautifulsoup4 and requests, from JSON can be used on mobile & web applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustusbs/latest-earthquake-indonesia",
    project_urls={
        "Bug Tracker": "https://remoteworker.id",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)