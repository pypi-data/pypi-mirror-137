from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='docums-nav-enhancements',
    version='0.9.1',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    description='This is a small plugin for the excellent Docums project which makes some enhancements to the navigation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/khanhduy1407/docums-nav-enhancements',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'docums>=1.0.0.0'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'docums.plugins': [
            'docums-nav-enhancements = docums_nav_enhancements:DocumsNavEnhancements'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Documentation'
    ],
)
