import setuptools


setuptools.setup(
    name='vjobs-vdnjobs',
    version='0.1.2',
    url='https://gitlab.com/flaxking/vjobs-vdnjobs',
    author='flaxking',
    author_email='flaxking@digitalnostril.com',
    description='Collects jobs from vdnjobs.ca for vjobs',
    long_description='Collects jobs from vdnjobs.ca for vjobs',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['vjobs >= 0.1.0', 'vdnjobs-client'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
