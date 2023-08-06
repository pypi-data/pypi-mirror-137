from setuptools import setup, find_packages

setup(
    name="nlp-utils-ch",
    version="1.1.0",
    description="nlp基础工具",
    author="peng.su",
    packages=find_packages(),
    # include_package_data=True,
    package_data={
                '':[
                    'zhconv/zhcdict.json',
                    'resources/*.txt'
                    ],
               
    			},
    install_requires=[
          'numba==0.49.1'
      ],
    author_email="alweeq5@163.com",
)
