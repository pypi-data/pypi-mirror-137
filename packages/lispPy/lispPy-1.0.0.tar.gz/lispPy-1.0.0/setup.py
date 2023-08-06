from setuptools import setup

setup(
    name='lispPy',
    version='1.0.0',    
    description='Toy Python Package for interpreting Lisp code, but with not as much power. Not meant for production use',
    url='https://github.com/RachitSharma2001/Interpreter',
    author='Rachit Sharma',
    author_email='rachitsharma613@gmail.com',
    license='BSD 2-clause',
    packages=['lispPy'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)