import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='rheia',
      version='0.0.16',
      description='Robust design optimization of renewable Hydrogen and dErIved energy cArrier systems',
      url='https://github.com/rheia-framework/RHEIA/tree/main',
      author='Diederik Coppitters',
      author_email='rheia.framework@gmail.com',
      package_dir={"": "src"},
      packages= setuptools.find_packages(where="src"),
      classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
      ],       
      install_requires=[
      'pyDOE',
      'deap',
      'numpy',
      'scipy',
      'sobolsequence'
      ],
      python_requires = ">=3.6",
      include_package_data=True,
      zip_safe=False)