from setuptools import find_packages, setup


setup(
    name='eyja-rethinkdb',
    zip_safe=True,
    version='0.1.11',
    description='RethinkDB Plugin for Eyja',
    url='https://gitlab.com/public.eyja.dev/eyja-rethinkdb',
    maintainer='Anton Berdnikov',
    maintainer_email='agratoth@yandex.ru',
    packages=find_packages(),
    package_dir={'eyja_rethinkdb': 'eyja_rethinkdb'},
    install_requires=[
        'eyja-internal>==0.4.4',
        'rethinkdb>=2.4.8',
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
