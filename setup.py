from setuptools import setup

setup(
    name='CNJFacil',
    version='0.1.4',
    author='Marcus Bodock',
    author_email='mbodock@gmail.com',
    packages=['cnjfacil'],
    url='https://github.com/mbodock/cnjfacil',
    license='MIT',
    description='Conjunto de ferramentas para trabalhar com CNJ',
    long_description=open('README.md').read(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['README.md']},
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
