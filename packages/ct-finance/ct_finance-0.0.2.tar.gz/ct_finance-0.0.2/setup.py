from distutils.core import setup

setup(name='ct_finance',
      version='0.0.2',
      packages=['ct_finance'],
      license='MIT',
      description='console based finance manager',
      author='Dan',
      author_email='daniel.js.campbell@gmail.com',
      url='https://github.com/dn757657/ct-data.git',
      download_url='https://github.com/dn757657/ct_finance/archive/refs/tags/0.0.2.tar.gz',
      keywords=['docopt', 'sqlite', 'ct-finance'],
      install_requires=[
            'pandas~=1.3.5',
            'pathlib~=1.0.1',
            'python-dateutil~=2.8.2',
            'docopt~=0.6.2',
            'web3~=5.26.0',
            'textblob~=0.17.1',
            'colorama~=0.4.4',
            'tabulate~=0.8.9',
      ],
      classifiers=[
            'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',      # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      )
