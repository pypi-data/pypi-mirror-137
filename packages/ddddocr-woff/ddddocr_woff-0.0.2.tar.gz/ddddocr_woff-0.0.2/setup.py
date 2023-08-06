import setuptools

setuptools.setup(
    name="ddddocr_woff",
    version="0.0.2",
    author="Fan&MuYiSen",
    descripyion="基于ddddocr的字体文件一键识别，适用于小白",
    long_description="基于ddddocr的字体文件一键识别，适用于小白",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(where='.', exclude=(), include=('*',)),
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    python_requires='<3.10',

)