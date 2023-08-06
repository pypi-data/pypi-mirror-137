from setuptools import setup

setup(
    name='radio-sdk',
    version='0.1.0',
    description='A Python SDK for the Radio Browser API',
    url="https://github.com/brendanjamesmulhern/radio_sdk",
    author='Brendan Mulhern',
    email="codedits93@gmail.com",
    py_modules=["radio_sdk"],
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)