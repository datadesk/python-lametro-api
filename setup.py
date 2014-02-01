from setuptools import setup, find_packages

setup(name='python-lametro-api',
      version='0.2.0',
      description='A simple Python wrapper for the L.A. Metro\'s API.',
      author='Ben Welsh',
      author_email='ben.welsh@latimes.com',
      url='http://datadesk.github.com/python-lametro-api/',
      packages=find_packages(),
      license='MIT',
      keywords='losangeles metro transit buses transportation',
      classifiers=["Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules"
                   ],
      install_requires=[
        'requests==2.0.0',
        'six==1.4.1',
      ],
     )
