from setuptools import setup, find_packages

setup(
	name='chesspos',
	version='0.1.3',
	description='A library for manipulating, learning and searching chess positions',
	url='https://github.com/patrickfrank1/chesspos/',
	author='Patrick Frank',
	author_email='patrickfrank1@outlook.com',
	license='GPLv3',
	packages=find_packages(),
	classifiers=[
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Software Development :: Pre-processors',
		'Topic :: Games/Entertainment :: Board Games'
	],
	zip_safe=False,
	python_requires='>=3.7',
	install_requires=[
		'chess',
		'colorama',
		'faiss',
		'h5py',
		'keras',
		'matplotlib',
		'numpy',
		'scikit_learn',
		'setuptools',
		'tensorflow',
		'pyyaml'
	]
)
