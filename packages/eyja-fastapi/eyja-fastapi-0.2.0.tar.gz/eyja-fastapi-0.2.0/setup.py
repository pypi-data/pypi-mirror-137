from setuptools import setup, find_packages


setup(
    name='eyja-fastapi',
    zip_safe=True,
    version='0.2.0',
    description='Eyja bindings for FastAPI',
    url='https://gitlab.com/public.eyja.dev/eyja-fastapi-users',
    maintainer='Anton Berdnikov',
    maintainer_email='agratoth@yandex.ru',
    packages=find_packages(),
    package_dir={'eyja_fastapi': 'eyja_fastapi'},
    install_requires=[
        'eyja-internal>=0.5.0',
        'eyja-email>=0.1.0',
        'fastapi>=0.70.1',
        'passlib>=1.7.4',
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
