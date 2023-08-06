from setuptools import setup

setup(
	name='newpipelist',
	description='A utility to convert playlists in a NewPipe database export to M3U files',
	version='1.0',
	author='Gwyneth Morgan',
	author_email='gwymor@tilde.club',
	url='https://tilde.club/~gwymor/newpipelist',
	py_modules=['newpipelist'],
	entry_points={'console_scripts': ['newpipelist=newpipelist:main']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	]
)
