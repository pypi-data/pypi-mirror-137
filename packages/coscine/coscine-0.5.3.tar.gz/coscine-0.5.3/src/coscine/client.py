###############################################################################
# Coscine Python SDK
# Copyright (c) 2018-2021 RWTH Aachen University
# Git: https://git.rwth-aachen.de/coscine/docs/public/coscine-python-sdk
# Please direct bug reports, feature requests or questions at the URL above
# by opening an issue.
#
# Coscine is an open source project at RWTH Aachen University for
# the management of research data.
# Visit https://www.coscine.de for more information.
#
# Please note that this python module resembles a community effort
# and not an official service that RWTH Aachen provides support for.
# It has been initially brough to life by the team at Coscine but has since
# been turned over to the community around Coscine.
###############################################################################

from typing import Iterable
import urllib
import requests
import json

from .static import StaticServer
from .project import Project, ProjectForm
from .version import __version__
from .banner import BANNER
from .exceptions import *

###############################################################################

class Client:

	"""
	The client class is the backbone and manager of the SDK and mainly
	responsible for the communication and exchange of information 
	with Coscine servers.

	Attributes
	-----------
	lang : str, "en" or "de"
		Language preset for input forms and form data.
	verbose : bool
		Enables/Disables command line output such as log data.
	version : str
		Contains the current version string of the python SDK.
	static : coscine.StaticServer
		Retrieves data from Coscine that rarely/never changes.
	"""

	lang: str
	verbose: bool
	session: requests.Session
	loglevel: Iterable[str]
	version: str
	static: StaticServer

###############################################################################

	def __init__(self, token: str, lang: str = "en", verbose: bool = False,
		loglevel: Iterable[str] = ["LOG", "INFO", "WARN", "REQUEST", "DATA"],\
									persistent_caching: bool = False) -> None:
		"""
		The base class of the Coscine Python SDK. When called it
		creates a new Coscine client object.

		Parameters
		----------
		token : str
			Coscine API access token
		lang : str, "en" or "de", default: "en"
			Language preset for input form fields.
		verbose : bool, default: False
			Enables verbose mode - logging/printing information to stdout.
		loglevel : str
			Enables which messages are printed in verbose mode.
			By default all levels are enabled. Possible values:
			Any combination of values inside an Iterable:
			["LOG", "INFO", "WARN", "REQUEST", "DATA"]
		persistent_caching : bool
			Enable to store the cache in a file on deinitialization of
			the client object. Will attempt to load the cache file
			on initialization if enabled. Leads to a significant speed
			boost when making static requests right after init, but may
			also lead to invalid data when using old cache, in case
			the Coscine API changed. Useful for applications with
			a short runtime which get run often.
		"""

		LANG = ("en", "de")
		if type(token) is not str:
			raise TypeError("Expected argument 'token' as string!")
		if lang not in LANG:
			raise ValueError("Invalid value for argument 'lang'! "\
							"Possible values are %s." % str(LANG))

		self.version = __version__
		self.lang = lang
		self.verbose = verbose
		self.loglevel = loglevel
		self.static = StaticServer(self, persistent_caching)
		self.session = requests.Session()
		self.session.headers = {
			"Authorization": "Bearer " + token,
			"User-Agent": "Coscine Python SDK %s" % self.version
		}
		self.log(BANNER)

###############################################################################

	def log(self, msg: str, level: str = None) -> None:
		"""
		Prints a message to stdout if verbose mode is enabled.

		Parameters
		----------
		msg : str
			Message as a string.
		level :	str, default: None
			Which loglevel to use for printing.
			Possible values: "LOG", "INFO", "WARN",	"REQUEST", "DATA", None
		"""

		LOGLEVELS = ["LOG", "INFO", "WARN", "REQUEST", "DATA"]

		if not self.verbose:
			return
		if level is None:
			print(msg)
		elif self.verbose and level in LOGLEVELS:
			print("[%s] %s" % (level, msg))
		else:
			raise ValueError("Invalid value for argument 'level'! "\
						"Possible values are %s." % str(LOGLEVELS))

###############################################################################

	def latest_version(self) -> str:
		"""
		Retrieves the version string of the latest version of this
		package hosted on PyPi. Useful for checking whether the currently
		used version is outdated and if an update should be performed.

		Examples
		--------
		>>> if client.version != client.latest_version():
		>>> 	print("Module outdated.")
		>>> 	print("Run 'py -m pip install --upgrade coscine'.")
		```

		Returns
		-------
		str
			The version string of the Coscine Python SDK hosted on PyPi.
		"""

		URI = "https://pypi.org/pypi/coscine/json"
		data = requests.get(URI).json()
		version = data["info"]["version"]
		return version

###############################################################################

	@staticmethod
	def uri(api: str, endpoint: str, *args) -> str:
		"""
		Constructs a URL for performing a request to the Coscine API.

		Parameters
		----------
		api : str
			The target Coscine API endpoint.
		endpoint : str
			The subendpoint of `api`.
		*args
			Variable number of arguments of type string to append to the URL.
			Arguments are automatically seperated by a slash '/' and
			special characters are encoded.
		
		Returns
		-------
		str
			Encoded URL for communicating with Coscine servers.
		"""

		BASE = "https://coscine.rwth-aachen.de/coscine/api/Coscine.Api.%s/%s"
		ENDPOINTS = (
			"Blob",
			"Metadata",
			"Organization",
			"Project",
			"Resources",
			"Tree",
			"User",
			"ActivatedFeatures"
		)

		if api not in ENDPOINTS:
			raise ValueError("Invalid value for argument 'api'. "\
						"Possible values are %s." % str(ENDPOINTS))

		uri = BASE % (api, endpoint)
		for arg in args:
			if arg is None:
				continue
			uri += "/" + urllib.parse.quote(arg, safe="")

		return uri

###############################################################################

	def _request(self, method: str, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a HTTP request to the Coscine Servers.

		Parameters
		----------
		method : str
			HTTP request method.
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		self.log("%s %s" % (method, uri), "REQUEST")

		if "data" in kwargs and type(kwargs["data"]) is dict:
			kwargs["headers"] = {
				"Content-Type": "application/json;charset=utf-8"
			}
			kwargs["data"] = json.dumps(kwargs["data"])
			self.log(json.dumps(kwargs["data"], indent=4), "DATA")

		try:
			response = self.session.request(method, uri, **kwargs)
			response.raise_for_status()
			return response
		except requests.exceptions.ConnectionError:
			raise ConnectionError()
		except requests.exceptions.RequestException as e:
			if e.response.status_code == 401:
				raise AuthorizationError("Invalid API token!")
			else:
				raise ClientError()

###############################################################################

	def get(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a GET request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		>>> uri = client.uri("Project", "Project")
		>>> projects = client.get(uri).json()

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("GET", uri, **kwargs)

###############################################################################

	def put(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a PUT request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		>>> uri = self.client.uri("Tree", "Tree", resource.id, filename)
		>>> self.client.put(uri, data = metadata)

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("PUT", uri, **kwargs)

###############################################################################

	def post(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a POST request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional arguments forwarded to the requests library.
		
		Examples
		--------
		TODO

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("POST", uri, **kwargs)

###############################################################################

	def delete(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a DELETE request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		TODO

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("DELETE", uri, **kwargs)

###############################################################################

	def projects(self, toplevel: bool = True, **kwargs) -> Iterable[Project]:
		"""
		Retrieves a list of a all projects the creator of the Coscine API token
		is currently a member of.

		Parameters
		----------
		toplevel : bool, default: True
			Retrieve only toplevel projects (no subprojects).
			Set to False if you want to retrieve all projects, regardless
			of hierarchy.
		**kwargs
			Project filter values.
			-> e.g. displayName="MyProject"
			-> Returns all projects with the specified displayName

		Returns
		-------
		list
			List of coscine.Project objects
		"""

		ENDPOINTS = ("Project", "Project/-/topLevel")
		uri = self.uri("Project", ENDPOINTS[toplevel])
		projects = []
		for entry in self.get(uri).json():
			for key, value in kwargs.items():
				if entry[key] != value:
					break
			else:
				projects.append(Project(self, entry))
		return projects

###############################################################################

	def project(self, displayName: str = None, toplevel: bool = True, \
												**kwargs) -> Project:
		"""
		Retrieves a single project the holder of the Coscine
		API token is currently a member of. Search criteria
		must be specified.

		Parameters
		----------
		toplevel : bool, default: True
			Search only within toplevel projects (no subprojects)
			Set to False if you want to search through all projects,
			regardless of hierarchy.
		**kwargs (mandatory!)
			Project filter values.
			-> e.g. displayName="MyProject"
			-> Returns one project matching the specified displayName

		Raises
		-------
		coscine.exceptions.AmbiguityError
			If more than one project match the specified search criteria.

		Returns
		-------
		coscine.Project
			coscine.Project object if a project matches the specifed filter.
		None
			if no project matching the filter was found.
		"""

		if displayName:
			kwargs["displayName"] = displayName
		elif not kwargs:
			raise ParameterError("Not enough arguments!")
		projects = self.projects(toplevel, **kwargs)
		if len(projects) == 1:
			return projects[0]
		elif len(projects) == 0:
			return None
		else:
			raise AmbiguityError("Found more than 1 project matching "\
											"the specified criteria!")

###############################################################################

	def create_project(self, form: ProjectForm) -> Project:
		"""
		Creates a project using the given ProjectForm.

		Parameters
		----------
		form : coscine.ProjectForm
			ProjectForm filled with project metadata.

		Returns
		-------
		coscine.Project
			Project object of the new project.
		"""

		if type(form) is ProjectForm:
			form = form.generate()
		
		uri = self.uri("Project", "Project")
		return Project(self, self.post(uri, data=form).json())

###############################################################################

	def ProjectForm(self, parent: Project = None) -> ProjectForm:
		"""
		Generates a project form to create and edit project metadata.

		Parameters
		----------
		parent : coscine.Project, default: None
			A parent Coscine project.
		
		Returns
		--------
		coscine.ProjectForm
		"""

		return ProjectForm(self, parent)

###############################################################################