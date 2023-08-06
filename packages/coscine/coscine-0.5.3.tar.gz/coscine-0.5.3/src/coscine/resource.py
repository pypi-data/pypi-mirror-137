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

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, List
if TYPE_CHECKING:
	from .client import Client
	from .project import Project
import os
import json
from prettytable import PrettyTable
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from .object import Object
from .form import InputForm
from .metadata import MetadataForm
from .exceptions import *
from .progressbar import ProgressBar

###############################################################################

class Resource:
	"""
	Coscine Resource type.

	Attributes
	----------
	id : str
		Coscine-internal resource-ID
	pid : str
		Persistent Identifier of the resource
	"""

	client: Client
	project: Project
	data: dict
	id: str
	pid: str
	name: str
	displayName: str
	type: str
	disciplines: List[str]
	profile: str
	archived: bool
	creator: str
	s3: S3info

###############################################################################

	class S3info:
		access_key: str = ""
		secret_key: str = ""
		endpoint: str	= ""
		bucket: str		= ""
		
		def __init__(self, data: dict) -> None:
			if "resourceTypeOption" in data and data["resourceTypeOption"]:
				self.access_key = data["resourceTypeOption"].get("WriteAccessKey")
				self.secret_key = data["resourceTypeOption"].get("WriteSecretKey")
				self.endpoint = data["resourceTypeOption"].get("Endpoint")
				self.bucket = data["resourceTypeOption"].get("BucketName")

###############################################################################

	def __init__(self, project: Project, data: dict) -> None:
		"""
		Initializes the Resource object

		Parameters
		----------
		project : coscine.Project
			Coscine project handle
		data : dict
			Coscine resource data.
		"""

		self.client = project.client
		self.project = project
		self.data = data
		self.id = data["id"]
		self.pid = data["pid"]
		self.name = data["resourceName"]
		self.displayName = data["displayName"]
		self.license = data["license"]["displayName"] \
						if self.data["license"] else ""
		self.type = self.data["type"]["displayName"]
		self.disciplines = [k["displayNameEn"] for k in data["disciplines"]]
		self.profile = self.data["applicationProfile"]
		self.archived = self.data["archived"]
		self.creator = self.data["creator"]
		self.s3 = Resource.S3info(data)

###############################################################################

	def __repr__(self) -> str:
		return self.__str__()

###############################################################################

	def __str__(self) -> str:
		table = PrettyTable(["Field", "Value"])
		rows = [
			("ID", self.id),
			("Resource Name", self.name),
			("Display Name", self.displayName),
			("PID", self.pid),
			("Type", self.type),
			("Disciplines", "\n".join(self.disciplines)),
			("License", self.license),
			("Application Profile", self.profile),
			("Archived", self.archived),
			("Creator", self.creator)
		]
		table.max_width["Value"] = 50
		table.add_rows(rows)
		return table.get_string(title = "Resource")

###############################################################################

	def upload(self, key: str, file, metadata: dict = None, \
					callback: Callable[[int]] = None) -> None:
		"""
		Uploads a file-like object to a resource on the Coscine server

		Parameters
		----------
		key : str
			filename of the file-like object.
		file : object with read() attribute
				Either open file handle or local file location path.
		metadata : dict
			File metadata. For rds-s3 this is optional, but recommended.
		callback : Callable[int]
			Optional callback called during chunk uploads.
		"""

		if hasattr(file, "read"):
			fd = file
			filename = "MEM"
		elif type(file) is str:
			fd = open(file, "rb")
			filename = file
		else:
			raise TypeError("Argument `file` has unexpected type!")

		if metadata:
			if type(metadata) is MetadataForm:
				metadata = metadata.generate()
			uri = self.client.uri("Tree", "Tree", self.id, key)
			self.client.put(uri, data = metadata)

		uri = self.client.uri("Blob", "Blob", self.id, key)
		fields = {"files": (key, fd, "application/octect-stream")}
		encoder = MultipartEncoder(fields = fields)
		bar = ProgressBar(self.client, encoder.len, filename, "UP", callback)
		monitor = MultipartEncoderMonitor(encoder, callback = lambda monitor: \
										bar.update(monitor.bytes_read - bar.n))
		headers = {"Content-Type": monitor.content_type}
		self.client.put(uri, data = monitor, headers = headers)

###############################################################################

	def download(self, path: str = "./", metadata: bool = False) -> None:
		"""
		Downloads the resource and all of its contents to the local harddrive.

		Parameters
		----------
		path : str, default: "./"
			Path to the local storage location.
		metadata : bool, default: False
			If enabled, resource metadata is downloaded and put in
			a hidden file '.metadata.json'.
		"""

		path = os.path.join(path, self.name)
		if not os.path.isdir(path):
			os.mkdir(path)
		for file in self.objects():
			file.download(path)
		if metadata:
			data = json.dumps(self.data, indent=4)
			fd = open(os.path.join(path, ".resource-metadata.json"), "w")
			fd.write(data)
			fd.close()

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the Coscine resource and all objects contained within it.
		"""

		uri = self.client.uri("Resources", "Resource", self.id)
		self.client.delete(uri)

###############################################################################

	def quota(self) -> int:
		"""
		Retrieves the used up quota of the resource.

		Returns
		-------
		int
			Used up quota in bytes.
		"""

		uri = self.client.uri("Blob", "Blob", self.id, "quota")
		data = self.client.get(uri).json()
		return int(data["data"]["usedSizeByte"])

###############################################################################

	def objects(self, path: str = None, **kwargs) -> List[Object]:
		"""
		Returns a list of Objects stored within the resource

		Parameters
		------------
		kwargs
			file-object filter arguments (e.g. 'Name' = 'testfile').

		Returns
		-------
		list[Object]
			List of Coscine file-like objects.
		"""

		objects = []
		uri = self.client.uri("Tree", "Tree", self.id)
		if path:
			args = {"path": path}
		else:
			args = None
		data = self.client.get(uri, params = args).json()
		fileStorage = data["data"]["fileStorage"]
		metadataStorage = data["data"]["metadataStorage"]
		for data in fileStorage:
			for key, value in kwargs.items():
				if data[key] != value:
					break
			else:
				objects.append(Object(self, data))
		return objects

###############################################################################

	def object(self, displayName: str = None, path: str = None, **kwargs) \
																 -> Object:
		"""
		Returns an Object stored within the resource

		Parameters
		------------
		displayName : str, default: None
			file-object display name (filename/key).
		kwargs
			Filter

		Returns
		-------
		coscine.Object
			Python representation of the file-object as an Object instance
		"""
		
		if displayName:
			if displayName.endswith("/"):
				displayName = displayName[:-1]
			kwargs["Name"] = displayName
		elif not kwargs:
			raise ParameterError("")

		objects = self.objects(path=path, **kwargs)
		if len(objects) == 1:
			return objects[0]
		elif len(objects) == 0:
			return None
		else:
			raise AmbiguityError("Found more than 1 resource matching "\
											"the specified criteria!")

###############################################################################

	def application_profile(self, parse: bool = False) -> dict:
		"""
		Returns the application profile of the resource

		Parameters
		----------
		parse : bool, default: False
			Parse the profile into a more readable format.

		Returns
		--------
		dict
			Application profile of the resource, either parsed or raw.
		"""

		return self.client.static.application_profile(\
						self.profile, self.id, parse)

###############################################################################

	def form(self) -> ResourceForm:
		"""
		Returns a ResourceForm filled with the metadata of the current resource.

		Returns
		-------
		coscine.resource.ResourceForm
		"""

		form = ResourceForm(self.project)
		form.parse(self.data)
		return form

###############################################################################

	def update(self, form: ResourceForm) -> None:
		"""
		Updates the metadata of the resource using the supplied ResourceForm.

		Parameters
		----------
		form : coscine.resource.ResourceForm
			ResourceForm filled with updated values.
		"""

		if type(form) is ResourceForm:
			form = form.generate()
		elif type(form) is not dict:
			raise TypeError("")

		uri = self.client.uri("Resources", "Resource", self.id)
		self.client.post(uri, data = form)

###############################################################################

	def set_archived(self, flag: bool) -> None:
		"""
		Set the archived flag of the resource to put it in read-only mode.
		Only the resource creator or project owner can do this.

		Parameters
		----------
		flag : bool
			Enable with True, Disable with False.
		"""

		uri = self.client.uri("Resources", "Resource", self.id, \
					"setReadonly?status=%s" % str(flag).lower())
		self.client.post(uri)
		#self.data["archived"] = flag
		self.archived = flag

###############################################################################

	def MetadataForm(self, data: dict = None) -> MetadataForm:
		"""
		Creates a MetadataForm for this resource.

		Returns
		-------
		coscine.MetadataForm
		"""

		return MetadataForm(self, data)

###############################################################################

KEYS = [{
		"name": {
			"de": "Ressourcentyp",
			"en": "Resource Type"
		},
		"flags": InputForm.REQUIRED | InputForm.CONTROLLED,
		"field": "type"
	},{ # This is REQUIRED for rds and s3, but not for Linked Data!
		"name": {
			"de": "Ressourcengröße",
			"en": "Resource Size"
		},
		"flags": InputForm.SPECIAL,
		"field": "resourceTypeOption"
	},{
		"name": {
			"de": "Ressourcenname",
			"en": "Resource Name"
		},
		"flags": InputForm.REQUIRED,
		"field": "ResourceName"
	},{
		"name": {
			"de": "Anzeigename",
			"en": "Display Name"
		},
		"flags": InputForm.REQUIRED,
		"field": "DisplayName"
	},{
		"name": {
			"de": "Ressourcenbeschreibung",
			"en": "Resource Description"
		},
		"flags": InputForm.REQUIRED,
		"field": "Description"
	},{
		"name": {
			"de": "Disziplin",
			"en": "Discipline"
		},
		"flags": InputForm.REQUIRED | InputForm.CONTROLLED | InputForm.LIST,
		"field": "Disciplines"
	},{
		"name": {
			"de": "Ressourcenschlagwörter",
			"en": "Resource Keywords"
		},
		"flags": InputForm.NONE,
		"field": "Keywords"
	},{
		"name": {
			"de": "Lizenz",
			"en": "License"
		},
		"flags": InputForm.CONTROLLED,
		"field": "License"
	},{
		"name": {
			"de": "Verwendungsrechte",
			"en": "Usage Rights"
		},
		"flags": InputForm.NONE,
		"field": "UsageRights"
	},{
		"name": {
			"de": "Applikationsprofile",
			"en": "Application Profile"
		},
		"flags": InputForm.REQUIRED | InputForm.CONTROLLED,
		"field": "applicationProfile"
}]

MAP = {
	"description": "Description",
	"displayName": "DisplayName",
	"resourceName": "ResourceName",
	"keywords": "Keywords",
	"disciplines": "Disciplines",
	"license": "License",
	"resourceTypeOption": "resourceTypeOption",
	"applicationProfile": "applicationProfile",
	"type": "type",
	"usageRights": "UsageRights"
}

###############################################################################

class ResourceForm(InputForm):

	"""
	Coscine Input Form for creating and editing resources
	"""

###############################################################################

	def __init__(self, project: Project, data: dict = None) -> None:

		"""
		Initializes the Resource form. The fields are static and fixed.

		Parameters
		-----------
		project : coscine.Project
			Coscine project handle.
		"""

		vocabulary = {
			"type": project.client.static.resource_types(),
			"applicationProfile": project.client.static.application_profiles(),
			"License": project.client.static.licenses(),
			"Visibility": project.client.static.visibility(),
			"Disciplines": project.client.static.disciplines()
		}

		super().__init__("Resource Form", project.client.lang, KEYS, vocabulary)
		# Fill
		if data:
			for key in data:
				self[key] = data[key]

###############################################################################

	def parse(self, data: dict) -> None:

		"""
		Parses given resource data into a resource form.

		Parameters
		-----------
		data : dict
			Dict containing Coscine resource metadata (i.e. Resource.data).
		"""

		def _parse_disciplines(self, data):
			LSTR = {"en": "displayNameEn", "de": "displayNameDe"}[self._lang]
			disciplines = []
			for discipline in data:
				disciplines.append(discipline[LSTR])
			return disciplines

		for key in data:
			if key in MAP and data[key] != "":
				entry = self.entry(MAP[key])
				if entry is None:
					continue
				name = entry["name"][self._lang]
				flags = entry["flags"]
				value = data[key]
				if flags & InputForm.CONTROLLED or \
				flags & InputForm.LIST or \
				flags & InputForm.SPECIAL:
					if key == "disciplines":
						self[name] = _parse_disciplines(self, value)
					elif key == "resourceTypeOption":
						self[name] = value["Size"]
					elif key == "applicationProfile":
						values = list(self._vocabulary["applicationProfile"].values())
						keys = list(self._vocabulary["applicationProfile"].keys())
						position = values.index(value)
						self[name] = keys[position]
					elif value is not None and (key == "visibility"\
					 or key == "license" or key == "type"):
						self[name] = value["displayName"]
				else:
					self[name] = value

###############################################################################

	def generate(self) -> dict:

		"""
		Generates JSON-LD formatted representation of resource data

		Raises
		-------
		RequirementError
			When one or more required fields have not been set
		
		Returns
		--------
		dict
			JSON-LD formatted resource data
		"""

		def final_value(key, value):
			if self.is_controlled(key):
				return self._vocabulary[field][value]
			else:
				return value

		data = {}
		missing = []
		for key in self._keys:
			entry = self._keys[key]
			field = entry["field"]
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				value = self.store[key]
				if entry["flags"] & ResourceForm.LIST:
					if type(value) is not list and type(value) is not tuple:
						raise ValueError("Expected iterable value for key %s" % key)
					data[field] = []
					for v in value:
						data[field].append(final_value(key, v))
				else:
					data[field] = final_value(key, value)

		if missing:
			raise RequirementError(missing)

		size = {}
		if "resourceTypeOption" in data:
			size = {
				"Size": data["resourceTypeOption"]
			}
		elif data["type"]["displayName"] in ("rds", "rds-s3"):
			raise RequirementError("rds or rds-s3 require a size parameter!")
		data["resourceTypeOption"] = size

		data["Visibility"] = {
			"displayName": "Project Members",
			"id": "8ab9c883-eb0d-4402-aaad-2e4007badce6"
		}

		return data

###############################################################################