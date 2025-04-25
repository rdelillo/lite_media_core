import setuptools


setuptools.setup(
    name="lite_media_core",
    use_scm_version=True,
    description="A 'lite' framework to edit nodal graphs.",
    url='https://github.com/rdelillo/lite_media_core',
    packages=["lite_media_core"],
    include_package_data=True,
    install_requires=[
        "timecode",
        "fileseq==1.8.1",
        "pymediainfo",
    ],
    extras_require={
        "testing": ["pytest", "pytest-cov", "mock"],
        "embedded": ["requests", "validators", "yt-dlp"],
        "pylint": ["pylint"],
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],    
)
