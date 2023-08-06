from setuptools import setup

"""
python setup.py sdist
python setup.py install
twine upload dist/*
"""
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="eui",
    version="1.0.13",
    keywords=["pip", "eui"],
    description="a fast and simple micro-framework for small browser-based application",
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    license="MIT Licence",

    url="https://gitee.com/lixkhao/eui",
    author="Li Xiangkui",
    author_email="1749498702@qq.com",
    py_modules=['eui'],
    # packages=find_packages(),
    # include_package_data=True,
    platforms="any",
    install_requires=[]
)
