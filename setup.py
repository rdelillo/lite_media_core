import os
import setuptools


setuptools.setup(
    name="lite_media_core",
    use_scm_version=True,
    description="A 'lite' framework to edit nodal graphs.",
    url='https://gitlab.com/tp_packages/lite_media_core',
    packages=["lite_media_core"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "timecode==0.3.0",
        "fileseq==1.8.1",
        "pymediainfo==5.1.0",
        "requests",
        "six",
        "validators",
        "yt-dlp",
    ],
    extras_require={
        "testing": ["pytest", "pytest-cov", "mock"],
        "pylint": ["pylint"],
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
)
