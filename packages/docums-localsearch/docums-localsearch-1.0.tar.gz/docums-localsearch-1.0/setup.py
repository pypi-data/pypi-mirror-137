from setuptools import setup, find_packages

setup(
    name='docums-localsearch',
    version='1.0',
    description='A Docums plugin to replace the native "search" plugin with a search plugin that also works locally (file:// protocol). Only works with the Material theme.',
    long_description='',
    keywords='docums local search',
    url='https://github.com/khanhduy1407/docums-localsearch',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'docums>=1.1.0',
        'docurial>=8.1.8.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'docums.plugins': [
            'localsearch = docums_localsearch_plugin.plugin:LocalSearchPlugin'
        ]
    }
)
