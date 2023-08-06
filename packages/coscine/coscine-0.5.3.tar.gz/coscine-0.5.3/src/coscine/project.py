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
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
	from .client import Client
	from . import ProjectForm

import os
import json
from prettytable import PrettyTable

from .metadata import MetadataPresetForm
from .exceptions import *
from .resource import Resource, ResourceForm
from .form import InputForm

###############################################################################

class Project:
	"""
	Python representation of a Coscine Project
	"""

	client: Client
	data: dict
	parent: Project
	id: str
	name: str
	displayName: str
	description: str
	principleInvestigators: str
	startDate: str
	endDate: str
	disciplines: List[str]
	organizations: List[str]
	visibility: str

###############################################################################

	def __init__(self, client: Client, data: dict, parent: Project = None) -> None:
		"""
		Initializes a project object.

		Parameters
		----------
		client : coscine.Client
			Coscine client handle
		data : dict
			Project data received from Coscine.
		parent : coscine.Project
			Optional parent project.
		"""

		self.client = client
		self.data = data
		self.parent = parent
		self.id = data["id"]
		self.name = data["projectName"]
		self.displayName = data["displayName"]
		self.description = data["description"]
		self.principleInvestigators = data["principleInvestigators"]
		self.startDate = data["startDate"]
		self.endDate = data["endDate"]
		self.disciplines = [k["displayNameEn"] for k in data["disciplines"]]
		self.organizations = [k["displayName"] for k in data["organizations"]]
		self.visibility = data["visibility"]["displayName"]

###############################################################################

	def __repr__(self) -> str:
		return self.__str__()

###############################################################################

	def __str__(self) -> str:
		table = PrettyTable(("Field", "Value"))
		rows = [
			("id", self.id),
			("Name", self.name),
			("Display Name", self.displayName),
			("Principle Investigators", self.principleInvestigators),
			("Disciplines", "\n".join(self.disciplines)),
			("Organizations", "\n".join(self.organizations)),
			("Start date", self.startDate),
			("End date", self.endDate)
		]
		table.max_width["Value"] = 50
		table.add_rows(rows)
		return table.get_string(title="Project")

###############################################################################

	def subprojects(self, **kwargs) -> List[Project]:
		"""
		Retrieves a list of subprojects of the current project matching a set
		of specified filters

		Parameters
		----------
		kwargs
			key-value filters for subprojects (e.g. 'Name' = 'My Project').

		Returns
		-------
		list of coscine.Project
		"""

		uri = self.client.uri("Project", "SubProject", self.id)
		projects = self.client.get(uri).json()
		filter = []
		for data in projects:
			match = True
			for key, value in kwargs.items():
				if data[key] != value:
					match = False
					break
			if match:
				filter.append(Project(self.client, data, self))
		return filter

###############################################################################

	def resources(self, **kwargs) -> List[Resource]:
		"""
		Retrieves a list of Resources of the current project matching a set
		of specified filters.

		Parameters
		----------
		kwargs
			key-value filters for resources (e.g. 'Name' = 'My Resource').
		
		Returns
		-------
		list[coscine.Resource]
			list of resources matching the supplied filter.
		"""

		uri = self.client.uri("Project", "Project", self.id, "resources")
		resources = []
		for data in self.client.get(uri).json():
			for key, value in kwargs.items():
				if data[key] != value:
					break
			else:
				resources.append(Resource(self, data))
		return resources

###############################################################################

	def resource(self, displayName: str = None, **kwargs) -> Resource:
		"""
		Retrieves a certain resource of the current project matching a set
		of specified filters or identified by its displayName.

		Parameters
		----------
		displayName : str
			The display name of the resource.
		kwargs
			key-value filters for resources (e.g. 'Name' = 'My Resource').
		
		Returns
		--------
		coscine.Resource or None
		"""
		
		if displayName:
			kwargs["displayName"] = displayName
		elif not kwargs:
			raise ParameterError("")

		resources = self.resources(**kwargs)
		if len(resources) == 1:
			return resources[0]
		elif len(resources) == 0:
			return None
		else:
			raise AmbiguityError("Found more than 1 resource matching "\
											"the specified criteria!")

###############################################################################

	def download(self, path: str = "./", metadata: bool = False) -> None:
		"""
		Downloads the project to the location referenced by 'path'.

		Parameters
		----------
		path : str
			Download location on the harddrive
			Default: current directory './'
		metadata : bool, default: False
			If enabled, project metadata is downloaded and put in
			a hidden file '.metadata.json'.
		"""

		path = os.path.join(path, self.displayName)
		if not os.path.isdir(path):
			os.mkdir(path)
		for resource in self.resources():
			resource.download(path=path, metadata=metadata)
		if metadata:
			data = json.dumps(self.data, indent=4)
			fd = open(os.path.join(path, ".metadata.json"), "w")
			fd.write(data)
			fd.close()

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the project on the remote server.
		"""

		uri = self.client.uri("Project", "Project", self.id)
		self.client.delete(uri)

###############################################################################

	def members(self) -> List[ProjectMember]:
		"""
		Retrieves a list of all members of the current project

		Returns
		--------
		list of coscine.project.ProjectMember
			List of project members as ProjectMember objects.
		"""

		uri = self.client.uri("Project", "ProjectRole", self.id)
		data = self.client.get(uri).json()
		members = [ProjectMember(self, m) for m in data]
		return members

###############################################################################

	def invite(self, email: str, role: str = "Member") -> None:
		"""
		Invites a person to a project via their email address

		Parameters
		----------
		email : str
			The email address to send the invite to
		role : str, "Member" or "Owner", default: "Member"
			The role for the new project member
		"""

		ROLES = {
			"Owner": "be294c5e-4e42-49b3-bec4-4b15f49df9a5",
			"Member": "508b6d4e-c6ac-4aa5-8a8d-caa31dd39527"
		}

		if role not in ROLES:
			raise ValueError("Invalid role '%s'." % role)

		uri = self.client.uri("Project", "Project", "invitation")
		data = {
			"projectId": self.data["id"],
			"role": ROLES[role],
			"email": email
		}

		try:
			self.client.log("Inviting [%s] as [%s] to project [%s]." % 
												(email, role, self.id))
			self.client.post(uri, data = data)
		except ServerError:
			self.client.log("User [%s] has invite pending." % email)

###############################################################################

	def create_resource(self, form: ResourceForm, metadataPreset: \
							MetadataPresetForm = None) -> Resource:
		"""
		Creates a resource within the current project using the supplied
		resource form.

		Parameters
		----------
		resourceForm : coscine.ResourceForm
			Form to generate the resource with.
		metadataPreset : coscine.MetadataPresetForm
			optional application profile configuration.
		"""
		if type(form) is ResourceForm:
			form = form.generate()
		if metadataPreset:
			if type(metadataPreset) is MetadataPresetForm:
				metadataPreset = metadataPreset.generate()
			form["fixedValues"] = metadataPreset
		uri = self.client.uri("Resources", "Resource", "Project", self.id)
		return Resource(self, self.client.post(uri, data = form).json())

###############################################################################

	def form(self) -> ProjectForm:
		"""
		Returns a ProjectForm filled with metadata of the current project.
		"""
		form = ProjectForm(self.client)
		form.parse(self.data)
		return form

###############################################################################

	def update(self, form: ProjectForm) -> None:
		"""
		Updates a project using the given ProjectForm

		Parameters
		----------
		form : coscine.ProjectForm
			ProjectForm containing updated data.
		"""

		if type(form) is ProjectForm:
			form = form.generate()
		uri = self.client.uri("Project", "Project", self.id)
		self.client.post(uri, data = form)

###############################################################################

	def ResourceForm(self, data: dict = None) -> ResourceForm:
		"""
		Creates a ResourceForm for this project.

		Returns
		-------
		coscine.ResourceForm
		"""

		return ResourceForm(self, data)

###############################################################################

class ProjectMember:

	"""
	Initializes a project member for a given project.

	Parameters
	----------
	project : coscine.Project
		Coscine python SDK project handle.
	data: dict
		User data as dict, retrieved via 
		client.uri("Project", "ProjectRole", self.id).
	"""

	name: str
	email: str
	id: str
	role: str
	data: dict
	client: Client
	project: Project

	def __init__(self, project: Project, data: dict) -> None:
		"""
		"""

		self.project = project
		self.client = self.project.client
		self.data = data
		self.name = data["user"]["displayName"]
		self.email = data["user"]["emailAddress"]
		self.id = data["user"]["id"]
		self.role = data["role"]["displayName"]

###############################################################################

	def set_role(self, role: str) -> None:

		"""
		Sets the role of a project member

		Parameters
		----------
		role : str
			The new role of the member ('Owner' or 'Member').
		"""

		ROLES = {
			"Owner": "be294c5e-4e42-49b3-bec4-4b15f49df9a5",
			"Member": "508b6d4e-c6ac-4aa5-8a8d-caa31dd39527"
		}

		if role not in ROLES:
			raise ValueError("Invalid role '%s'." % role)

		uri = self.client.uri("Project", "ProjectRole")
		self.data["role"]["id"] = ROLES[role]
		self.data["role"]["displayName"] = role
		self.client.post(uri, data = self.data)

###############################################################################

	def remove(self) -> None:
		"""
		Removes a project member from their associated project.
		"""

		uri = self.client.uri("Project", "ProjectRole", "project", \
			self.project.id, "user", self.id, "role", self.data["role"]["id"])
		self.client.delete(uri)

###############################################################################

KEYS = [{
		"name": {
			"de": "Projektname",
			"en": "Project Name"
		},
		"flags": InputForm.REQUIRED,
		"field": "ProjectName"
	},{
		"name": {
			"de": "Anzeigename",
			"en": "Display Name"
		},
		"flags": InputForm.REQUIRED,
		"field": "DisplayName"
	},{
		"name": {
			"de": "Projektbeschreibung",
			"en": "Project Description"
		},
		"flags": InputForm.REQUIRED,
		"field": "Description"
	},{
		"name": {
			"de": "Principal Investigators",
			"en": "Principal Investigators"
		},
		"flags": InputForm.REQUIRED,
		"field": "PrincipleInvestigators"
	},{
		"name": {
			"de": "Projektstart",
			"en": "Project Start"
		},
		"flags": InputForm.REQUIRED,
		"field": "StartDate"
	},
	{
		"name": {
			"de": "Projektende",
			"en": "Project End"
		},
		"flags": InputForm.REQUIRED,
		"field": "EndDate"
	},{
		"name": {
			"de": "Disziplin",
			"en": "Discipline"
		},
		"flags": InputForm.REQUIRED | InputForm.CONTROLLED | InputForm.LIST,
		"field": "Discipline"
	},{
		"name": {
			"de": "Teilnehmende Organisation",
			"en": "Participating Organizations"
		},
		"flags": InputForm.REQUIRED | InputForm.CONTROLLED | InputForm.LIST,
		"field": "Organization"
	},{
		"name": {
			"de": "Projektschlagwörter",
			"en": "Project Keywords"
		},
		"flags": InputForm.NONE,
		"field": "Keywords"
	},{
		"name": {
			"de": "Grant ID",
			"en": "Grant ID"
		},
		"flags": InputForm.NONE,
		"field": "GrantId"
	},{
		"name": {
			"de": "Features",
			"en": "Features"
		},
		"flags": InputForm.CONTROLLED,
		"field": "Features"
}]

###############################################################################

MAP = {
	"description": "Description",
	"displayName": "DisplayName",
	"startDate": "StartDate",
	"endDate": "EndDate",
	"keywords": "Keywords",
	"projectName": "ProjectName",
	"principleInvestigators": "PrincipleInvestigators",
	"grantId": "GrantId",
	"disciplines": "Discipline",
	"organizations": "Organization"
}

###############################################################################

class ProjectForm(InputForm):

	"""
	The Coscine input form for interacting with projects. Set and modify
	project	settings.
	"""

	def __init__(self, client: Client, parent: Project = None, data: dict = None) -> None:
		self.client = client
		vocabulary = {
			"Discipline": self.client.static.disciplines(),
			"Organization": self.client.static.organizations(),
			"Visibility": self.client.static.visibility(),
			"Features": self.client.static.features()
		}
		super().__init__("Project Form", client.lang, KEYS, vocabulary)
		self.parent = parent
		# Fill
		if data:
			for key in data:
				self[key] = data[key]

###############################################################################

	def parse(self, data: dict):

		"""
		Parses given project data into a project form.

		Parameters
		-----------
		data : dict
			Dict containing Coscine project metadata (i.e. Project.data).
		"""

		def _parse_disciplines(self, data):
			LSTR = {"en": "displayNameEn", "de": "displayNameDe"}[self._lang]
			disciplines = []
			for discipline in data:
				disciplines.append(discipline[LSTR])
			return disciplines

		def _parse_organizations(self, data):
			organizations = []
			for organization in data:
				vocabulary = self._vocabulary["Organization"]
				for entry in vocabulary.values():
					if entry["url"] == organization["url"]:
						organizations.append(entry["displayName"])
			return organizations

		for key in data:
			if key in MAP and data[key] != "":
				entry = self.entry(MAP[key])
				if entry is None:
					continue
				name = entry["name"][self._lang]
				flags = entry["flags"]
				value = data[key]
				if flags & InputForm.CONTROLLED or flags & InputForm.LIST:
					if key == "disciplines":
						self[name] = _parse_disciplines(self, value)
					elif key == "organizations":
						self[name] = _parse_organizations(self, value)
					elif key == "visibility":
						self[name] = value["displayName"]
				else:
					self[name] = value

###############################################################################

	def generate(self) -> dict:

		"""
		Generates Coscine JSON-LD representation of form data. Such data
		can be sent to Coscine for processing.

		Returns
		-------
		dict
			JSON-LD metadata dict
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
				if entry["flags"] & ProjectForm.LIST:
					if type(value) is not list and type(value) is not tuple:
						raise ValueError("Expected iterable value for key %s" % key)
					data[field] = []
					for v in value:
						data[field].append(final_value(key, v))
				else:
					data[field] = final_value(key, value)

		if missing:
			raise RequirementError(missing)
		
		if self.parent:
			data["ParentId"] = self.parent.id

		data["Visibility"] = {
			"displayName": "Project Members",
			"id": "8ab9c883-eb0d-4402-aaad-2e4007badce6"
		}

		return data

###############################################################################