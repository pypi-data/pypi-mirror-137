import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fooddetection",
    version="0.0.3",
    author="Yuki-max",
    author_email="yuki65763933@gmail.com",
    description="This library makes it possible to detect food in an image and make the non-food parts transparent.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yuki-max/FoodDetection.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)