import setuptools

setuptools.setup(
    name="ddddocr_woff",
    version="0.0.5",
    author="Fan&MuYiSen",
    descripyion="Font file based on DDDDOCR one key recognition, suitable for small white",
    long_description="Font file based on DDDDOCR one key recognition, suitable for small white",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(where='.', exclude=(), include=('*',)),
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    python_requires='<3.10',

)