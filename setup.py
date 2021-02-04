from setuptools import setup, find_packages

setup(
    name='pandasconvenience',
    version='0.0.1',
    description='A convenience package for Pandas.',
    url='https://github.com/GitPushPullLegs/pandasconvenience',
    author='Joe Aguilar',
    author_email='jose.aguilar.6694@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas', 'pyodbc'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)