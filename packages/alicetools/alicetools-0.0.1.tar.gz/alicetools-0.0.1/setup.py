from setuptools import setup, find_packages

LICENSE = open('license.txt').read()

setup(
    name='alicetools',
    version='0.0.1',
    setup_requires='setuptools',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tqdm',
        'pandas',
        'scikit-image',
        'allensdk',
    ],
    scripts=['alicetools/mota.py'],
    description='Tools developped for ALICe platform.',
    long_description='MOTA',
    long_description_content_type='text/markdown',
    url='https://github.com/WyssCenter/MOTA',
    author='Jules Scholler',
    author_email='jules.scholler@wysscenter.ch',
    license=LICENSE,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    keywords='cell mapping, atlas',
    entry_points={
        'console_scripts': ['mota = alicetools.mota:main']
    }
)
