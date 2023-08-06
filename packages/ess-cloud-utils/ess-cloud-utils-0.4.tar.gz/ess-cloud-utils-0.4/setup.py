from setuptools import setup

setup(
    name='ess-cloud-utils',
    packages=['ess_cloud_utils'],
    version='0.4',
    description='Set of utils to support cloud deployments',
    author='Mykola Zelenku and Kamil Szewc',
    author_email='',
    license='Apache2',
    install_requires=['requests', 'py-eureka-client'],
    keywords=['ESS'],
    classifiers=[],
    python_requires='>=3.8',
)
