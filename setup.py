from setuptools import setup, find_packages

setup(
    name='para_detector',
    version='0.1.0',  # start with a low version, increase it whenever you make significant changes
    author='yixiang, xu',
    author_email='yixiang-xu@berkley.edu',
    description='Python package using text analysis software for detecting nonverbal communication cues in text.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # this is important for your README to render correctly on PyPI
    url='https://github.com/yixiang-xu/PARA',  # link to the project repo or website
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # choose a license
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pandas',
        'numpy',
        'regex',
        'nltk',
        'multiprocessing',
        'os',
        're',
        'sys',
        'collections',
        'nlk.corpus',
        'traceback'
        # any other dependencies the project has
    ],
    python_requires='>=3.6',  # minimum python version
)
