from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'Converting .py Code-Files to .png with Code-Highlighting.'



setup(
    name="etpy2png",
    version=VERSION,
    author="ExperTeach GmbH",
    author_email="et_dbu@web.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'nbconvert'
        ],
    keywords=['python', 'code', 'screenshot', 'png', 'py', 'code-highlighting'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
