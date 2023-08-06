import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="ddzl_project", #
    packages=["ddzl_project"],
    version="0.3",
    license='MIT',
    author="wangyu",
    author_email="wangyu@ddzl.com",
    description="ddzl_project",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=['ddzl_project'],
    python_requires='>=3.6',
    # install_requires=[
    #     'win32',
    # ],
)