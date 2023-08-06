import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="round_using_error",
    version="1.1.1",
    description="Output numbers +/- error with appropriate rounding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gutow/round_using_error",
    author="Jonathan Gutow",
    author_email="gutow@uwosh.edu",
    license="GPL-3.0+",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
