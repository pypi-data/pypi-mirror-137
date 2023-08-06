from setuptools import setup, find_packages

VERSION = '1.0.2' 
DESCRIPTION = 'Python package for various tools that will be used by Vestel Team'

# Setting up
setup(
        name="vdst-toolbox", 
        version=VERSION,
        author="Berkay Gokova",
        author_email='berkaygokova@gmail.com',
        description=DESCRIPTION,
        packages=find_packages(),
        download_url=f"https://github.com/berkaygkv/vdst-toolbox/archive/refs/tags/{VERSION}.tar.gz",
        url="https://github.com/berkaygkv/vdst-toolbox",
        install_requires=['pandas', 'numpy', 'matplotlib'],      
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)