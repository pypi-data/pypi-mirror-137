from setuptools import find_packages, setup


setup(
    name='eyja-filedb',
    zip_safe=True,
    version='0.1.0',
    description='JSON DB support plugin for Eyja',
    url='https://gitlab.com/public.eyja.dev/eyja-filedb',
    maintainer='Anton Berdnikov',
    maintainer_email='agratoth@yandex.ru',
    packages=find_packages(),
    package_dir={'eyja_filedb': 'eyja_filedb'},
    install_requires=[
        'eyja-internal>=0.4.4',
        'aiofiles>=0.8.0',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
