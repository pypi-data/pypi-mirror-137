import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pystop", 
    version="0.2.0",
    author="Nachuan Xiao, Lei Wang, Bin Gao, Xin Liu, and Ya-xiang Yuan",
    author_email="stmopt@foxmail.com",
    description="A Toolbox for Stiefel Manifold Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stmopt.gitee.io/",
    packages=setuptools.find_packages(),
    keywords=("optimization,manifold optimization,Stiefel manifold"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['numpy>=1.16', 'scipy'],
    data_files=[
            "LICENSE",
            "README.md"]
)