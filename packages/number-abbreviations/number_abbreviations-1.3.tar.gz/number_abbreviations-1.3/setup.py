from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='number_abbreviations',
      version='1.3',
      description='converts abreviated numbers to their full form',
      author='Josh Shrawder',
      author_email="joshshrawder@gmail.com",
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      package_dir={"": "src"},
      packages=find_packages(where="src"),
      include_package_data=True,
      zip_safe=False)




