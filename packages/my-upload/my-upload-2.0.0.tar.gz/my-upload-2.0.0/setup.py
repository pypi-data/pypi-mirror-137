# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="my-upload",
    version="2.0.0",
    description="上传文件到文件系统",
    author="hxl",
    maintainer="hxl",
    packages=find_packages(),
    license='MIT License',
    entry_points={
        'console_scripts': [
            'tupload=file_upload.upload:start'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
