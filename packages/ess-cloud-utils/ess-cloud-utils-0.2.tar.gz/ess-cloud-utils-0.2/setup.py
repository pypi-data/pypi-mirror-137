from setuptools import setup

setup(
    name='ess-cloud-utils',
    packages=['ess_cloud_utils'],
    version='0.2',
    description='Set of utils to support cloud deployments',
    author='Mykola Zelenku and Kamil Szewc',
    author_email='',
    license='Apache2',
    # url = ‘https://github.com/ssbothwell/BinPack',
    install_requires=['requests', 'py-eureka-client'],
    # download_url = ‘https://github.com/ssbothwell/BinPack/archive/0.3.3.tar.gz',
    keywords=['ESS'],
    classifiers=[],
    python_requires='>=3.8',
)
