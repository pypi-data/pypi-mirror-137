from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
    setup(
     name='hwn',  
     version='0.1.0',
     scripts=['hwn/__init__.py'],
     author="Amina Imam Abubakar",
     author_email="aminaimamabubakar@gmail.com",
     description="A hausa wordnet library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/meenah-imam/hwn",
     packages=find_packages(),
     data_files=[('', ['hwn/kamus.json'])],
     include_package_data=True,
    #  entry_points={
    #     'console_scripts': [
    #         'hwn=hausa:test',
    #     ]
    # },
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )