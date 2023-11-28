import setuptools

setuptools.setup(
    name="explorecourses",
    version="1.0.6",
    url="https://github.com/illiteratecoder/Explore-Courses-API",
    author="Jeremy Ephron",
    author_email="jeremye@stanford.edu",
    description="A Python API for Stanford Explore Courses",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
