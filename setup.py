from setuptools import setup, find_packages

setup(
    name='eider',
    version='0.1',
    description='',
    author='Amin Etesamian',
    author_email='aminetesamian1371@gmail.com',
    url='https://github.com/eteamin/eider',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=["twisted"],
    tests_require=[],
    include_package_data=True,
)
