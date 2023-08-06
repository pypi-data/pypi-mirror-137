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
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .resource import Resource
from .exceptions import *
from .form import InputForm

###############################################################################

class MetadataForm(InputForm):

	"""
	Input form for interacting with Metadata.
	"""

	def __init__(self, resource: Resource, data: dict = None) -> None:
		"""
		Initializes the Metadata form.

		Parameters
		-----------
		resource : coscine.Resource
			Coscine resource instance.
		data : dict (optional)
			Data to initialize the MetadataForm with.
			If the form accepts fields "Title" and "Author", data could
			be data = {"Title": "a", "Author": "b"}
		"""

		client = resource.client
		entries = []
		vocabulary = {}
		lang = resource.client.lang
		profile = resource.application_profile(parse = True)
		for element in profile["graph"]:
			flags = MetadataForm.NONE
			if "minCount" in element and element["minCount"] > 0:
				flags |= MetadataForm.REQUIRED
			if "maxCount" in element and element["maxCount"] > 1:
				flags |= MetadataForm.LIST

			if "class" in element:
				flags |= MetadataForm.CONTROLLED
				uri = element["class"]
				instance = client.static.instance(resource.project.id, uri)
				if lang not in instance or len(instance[lang]) == 0:
					lang = "en"
				voc = {}
				for rule in instance[lang]:
					voc[rule["name"]] = rule["value"]
				vocabulary[element["name"][lang]] = voc

			entry = {
				"name": element["name"],
				"path": element["path"],
				"field": element["name"][lang],
				"flags": flags,
				"order": element["order"],
				"datatype": element["datatype"],
				"type": element["type"]
			}
			entries.append(entry)

		# Sort the keys according to their application profile order
		entries = sorted(entries, key = lambda x: x["order"])
		super().__init__("Metadata Form", lang, entries, vocabulary)
		self.profile = profile

		# Fill
		if data:
			for key in data:
				self[key] = data[key]

###############################################################################

	def parse(self, data: dict) -> None:

		"""
		Parses JSON-LD metadata into a Metadata Input Form

		Parameters
		-----------
		data : dict
			JSON-LD metadata (as retrieved from Coscine).
		"""

		if data is None:
			return

		for path in data:
			for entry in self.profile["graph"]:
				if path == entry["path"]:
					key = entry["name"][self._lang]
					value = data[path][0]["value"]
					if self.is_controlled(key):
						voc = self.get_vocabulary(key)
						keys = list(voc.keys())
						values = list(voc.values())
						index = values.index(value)
						value = keys[index]
					self.store[key] = value
					break

###############################################################################

	def generate(self) -> dict:

		"""
		Generates JSON-LD metadata for use in Coscine.

		Returns
		-------
		dict
			JSON-LD formatted metadata
		"""

		metadata = {}
		RDFTYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

		# Set application profile type used by metadata
		metadata[RDFTYPE] = [{
			"type": "uri",
			"value": self.profile["id"]
		}]

		# Collect missing required fields
		missing = []

		# Set metadata fields
		for key in self._keys:
			entry = self._keys[key]
			field = entry["field"]
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				path = entry["path"]
				value = self.store[key]
				if entry["flags"] & MetadataForm.LIST:
					if type(value) is not list and type(value) is not tuple:
						raise ValueError("Expected iterable value for key %s" % key)
				if self.is_controlled(key):
					voc = self.get_vocabulary(key)
					value = voc[value]
				metadata[path] = [{
					"value": value,
					"datatype": entry["datatype"],
					"type": entry["type"]
				}]

		# Check missing field list
		if len(missing) > 0:
			raise RequirementError(missing)

		return metadata

###############################################################################

class MetadataPresetForm(InputForm):

	"""
	The MetadataPreset form allows for the configuration of default
	values in an application profile.
	"""

	def __init__(self, resource: Resource, data: dict = None) -> None:
		"""
		Initialized the MetadataPreset form.

		Parameters
		----------
		resource : coscine.Resource
			Coscine resource instance.
		data : dict, default: None, currently unused
			Data to initialize the form with.
			If the form accepts fields "Title" and "Author", data could
			be data = {"Title": "a", "Author": "b"}
		"""

		entries = []
		vocabulary = {}
		lang = resource.client.lang
		applicationProfile = resource.application_profile(parse = True)
		for element in applicationProfile["graph"]:
			flags = MetadataPresetForm.NONE
			if "minCount" in element and element["minCount"] > 0:
				flags |= MetadataPresetForm.REQUIRED
			if "maxCount" in element and element["maxCount"] > 1:
				flags |= MetadataPresetForm.LIST

			if "class" in element:
				flags |= MetadataPresetForm.CONTROLLED
				uri = element["class"]
				instance = resource.client.static.instance(uri)
				if lang not in instance or len(instance[lang]) == 0:
					lang = "en"
				voc = {}
				for rule in instance[lang]:
					voc[rule["name"]] = rule["value"]
				vocabulary[element["name"][lang]] = voc
			
			entry = {
				"name": element["name"],
				"path": element["id"],
				"flags": flags,
				"field": element["name"][lang],
				"order": element["order"],
				"datatype": element["datatype"],
				"type": element["type"],
				"locked": False,
				"enabled": True
			}
			entries.append(entry)

		# Sort the keys according to their application profile order
		entries = sorted(entries, key = lambda x: x["order"])
		super().__init__("Metadata Preset", lang, entries, vocabulary)
		self.profile = applicationProfile

###############################################################################

	def enable(self, key: str, enable: bool = True) -> None:

		"""
		Enables or disables a metadata field.

		Parameters
		-----------
		key : str
			Form field key name.
		lock : bool, default: True
			True to enable, False to disable
		"""

		self._keys[key]["enabled"] = enable

###############################################################################

	def lock(self, key: str, lock: bool = True) -> None:

		"""
		Locks a form fields value.

		Note
		----
		Currently has no effect.

		Parameters
		-----------
		key : str
			form field key name
		lock : bool, default: True
			True to lock, False to unlock
		"""

		self._keys[key]["locked"] = lock

###############################################################################

	def generate(self) -> dict:

		"""
		Generates JSON-LD formatted representation of MetadataPreset data.

		Raises
		-------
		RequirementError
			When one or more required fields have not been set.
		
		Returns
		--------
		dict
			JSON-LD formatted MetadataPreset data.
		"""

		metadata = {}

		# Set metadata fields
		for key in self._keys:
			field = self._keys[key]
			path = field["path"]

			if key not in self.store:
				value = None
				metadata[path] = {
					"https://purl.org/coscine/defaultValue": [],
					"https://purl.org/coscine/invisible": [{
						"type": "literal",
						"value": "0"
					}]
				}
				continue
			else:
				value = self.store[key]
			if self.is_controlled(key):
				voc = self.get_vocabulary(key)
				value = voc[value]
			trigger: str = ["1", "0"][self._keys[key]["enabled"]]
			metadata[path] = {
				"https://purl.org/coscine/defaultValue": [{
					"type": field["type"],
					"value": value
				}],
				"https://purl.org/coscine/invisible": [{
					"type": "literal",
					"value": trigger
				}]
			}

		return metadata

###############################################################################