from setuptools import setup, find_packages

setup(
    name='bin-maker',
    version='3.1.0',
    description='protect and speed up python source code',
    py_modules=["bin_maker"],
    long_description="protect and speed up python source code",
    url='',
    author='etherfurnace',
    author_email='core@etherfurnace.com',
    classifiers=[],
    keywords='',
    install_requires=['cython==0.29.21', 'PyInstaller==4.0'],
    extras_require={},
    packages=find_packages(),
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'bin-maker-build=bin_maker.build:build',
            'bin-maker-release=bin_maker.action:release',
            'bin-maker-package=bin_maker.action:package',
        ],
    },
    project_urls={},
)
