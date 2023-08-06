import setuptools

setuptools.setup(
	name="virstrain",
	version="1.12",
	author="Liao Herui",
	author_email="heruiliao2-c@my.cityu.edu.hk",
	description="An RNA/DNA virus strain-level identification tool for short reads.",
	long_description="VirStrain can be applied to identify RNA/DNA viral strains from short reads.",
	long_description_content_type="text/markdown",
	url="https://github.com/liaoherui/VirStrain",
	packages=setuptools.find_packages(),
	include_package_data=True,
	zip_safe=True,
	package_data={
		"VirStrain":['jellyfish-linux',"*.pl"]
	},
	install_requires=[
	'networkx==2.4',
	'numpy==1.17.3',
	'pandas==1.0.1',
	'biopython==1.74',
	'plotly==3.10.0',
	'matplotlib==3.1.2'
	],
	entry_points={
		'console_scripts':[
		'virstrain = VirStrain.VirStrain:main',
		'virstrain_build = VirStrain.VirStrain_build:main',
		]
		},
	classifiers=[
		"Programming Language :: Python :: 3",
		],
)
