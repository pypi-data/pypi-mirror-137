import setuptools
from src.coscine.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "coscine",
	version = __version__,
	description = "Coscine Python SDK",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Coscine",
	author_email = "coscine@itc.rwth-aachen.de",
	license = "MIT License",
	packages = setuptools.find_packages(where="src"),
	keywords = [
		"Coscine", "RWTH Aachen", "Research Data Management"
	],
	install_requires = [
		"requests",
		"requests-toolbelt",
		"tqdm",
		"colorama",
		"prettytable"
	],
	url = "https://git.rwth-aachen.de/coscine/docs/public/coscine-python-sdk",
	project_urls = {
		"Issues":  "https://git.rwth-aachen.de/coscine/docs/public/coscine-python-sdk/-/issues",
		"Wiki": "https://git.rwth-aachen.de/coscine/docs/public/coscine-python-sdk/-/wikis/home"
	},
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers"
	],
	package_dir = {"": "src"},
	python_requires = ">=3.6"
)