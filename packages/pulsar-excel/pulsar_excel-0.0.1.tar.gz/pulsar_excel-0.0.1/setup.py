from setuptools import setup, find_packages

setup(
    name='pulsar_excel',
    version='0.0.1',
    license='MIT',
    author="Gyeongmin Kim",
    author_email='kgm1306@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Gyeongmin-lucid/pulsar-pip',
    keywords='pulsar',
    install_requires=[
      'csv',
      'pandas',
    ],
)