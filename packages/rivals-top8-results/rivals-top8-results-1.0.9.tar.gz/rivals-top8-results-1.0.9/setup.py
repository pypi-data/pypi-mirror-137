import setuptools
from glob import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

resources_dir = r'C:/Users/Impasse/My Drive/Linguaggi/Python/Rivals Top 8 Results/src/rivals_top8_results/'

setuptools.setup(
    name="rivals-top8-results",
    version="1.0.9",
    author="Impasse52",
    author_email="giuseppe.termerissa@gmail.com",
    description="Small Pillow library useful in creating automatic Rivals of Aether Top 8 Results screens ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Impasse52/rivals-top8-results",
    project_urls={
        "Bug Tracker": "https://github.com/Impasse52/rivals-top8-results/issues",
    },
    package_dir={"": "src"},
    include_package_data=True,
    data_files=[('Resources', glob(r"./src/rivals_top8_results/Resources/**/**/**/**"))],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)