from setuptools import setup


with open('README.md') as infile:
    readme = infile.read()


setup(
    name='more_bisect',
    description=('A binary search extension of Python `bisect` module that '
                 'enables flexible comparisons.'),
    long_description=readme,
    long_description_content_type='text/markdown',
    version='0.1.0',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=2.7',
    keywords='bisect',
    author='Kaiwen Wu',
    author_email='kps6326@hotmail.com',
    packages=['more_bisect'],
)
