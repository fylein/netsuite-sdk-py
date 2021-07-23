import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ucnetsuitesdk',
    version='1.0.18',
    author='Underground Cellar',
    author_email='support@undergroundcellar.com',
    description='Python SDK for accessing the NetSuite SOAP webservice',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['netsuite', 'api', 'python', 'sdk'],
    url='https://github.com/mattclark-uc/netsuite-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=['zeep'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
