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
	from .client import Client

import os
import json
import urllib
import atexit
from .version import __version__

###############################################################################

class StaticServer:

	"""
	The purpose of the StaticServer class is to provide
	static data which is not subject to change. Initially a request is made
	to the Coscine REST API to query such data. Upon further requests a
	cached response is used to speed things up and reduce internet traffic.
	Dynamic data such as the metadata of a project cannot be cached as
	it may be invalidated by further requests or interactions with a
	different client such as the web interface.
	"""

	client: Client
	cache: dict
	persist: bool

	CACHEFILE = "./.coscine_python_sdk_%s-cache.json" % __version__

	def __init__(self, client: Client, persist: bool = False) -> None:
		"""
		Intializes the StaticServer with a Coscine SDK client handle.
		"""

		self.client = client
		self.persist = persist
		if persist:
			atexit.register(self.savestate)
			try:
				fd = open(self.CACHEFILE, "r")
				self.cache = json.loads(fd.read())
				fd.close()
			except FileNotFoundError:
				self.cache = {}
		else:
			self.cache = {}

###############################################################################

	def savestate(self) -> None:
		"""
		Saves the cache if the persist option is enabled
		"""

		if self.persist and self.cache:
			fd = open(self.CACHEFILE, "w")
			fd.write(json.dumps(self.cache))
			fd.close()

###############################################################################

	def disciplines(self) -> dict:
		"""
		Queries the scientific disciplines available for selection in Coscine.

		Returns
		-------
		dict
			Dictionary containing the disciplines as keys.
		"""

		LANG = {
			"de": "displayNameDe",
			"en": "displayNameEn"
		}

		uri = self.client.uri("Project", "Discipline")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data
		
		disciplines = {}
		lang = LANG[self.client.lang]
		for entry in data:
			disciplines[entry[lang]] = entry
		
		return disciplines

###############################################################################

	def organizations(self) -> dict:
		"""
		Queries the organizations (e.g. 'RWTH Aachen University') available
		for selection in Coscine.

		Returns
		-------
		dict
			A python dictionary containing the organizations as keys.
		"""

		uri = self.client.uri("Organization", "Organization")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache["organizations"] = data

		organizations = {}
		for entry in data["data"]:
			organizations[entry["displayName"]] = entry
		return organizations

###############################################################################

	def visibility(self) -> dict:
		"""
		Gets the key-value mapping of the Coscine project visibility field.

		Returns
		-------
		dict
			Key-value mapped Coscine project visibility field.
		"""

		uri = self.client.uri("Project", "Visibility")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data

		visibility = {}
		for entry in data:
			visibility[entry["displayName"]] = entry
		return visibility

###############################################################################

	def features(self) -> dict:
		"""
		Returns a mapping for activated features of Coscine projects.
		Activated features resemble for example the announcement board
		and the documents section.

		Returns
		-------
		dict
			Dictionary containing the available features.
		"""

		uri = self.client.uri("ActivatedFeatures", "ActivatedFeatures")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data

		features = {}
		for entry in data:
			features[entry[self.client.lang]] = entry
		return features

###############################################################################

	def licenses(self) -> dict:
		"""
		Returns a dictionary containing a list of licenses available in Coscine
		as keys. The dictionary is supposed to be used for mapping license names
		to their internal representation in Coscine.

		Returns
		-------
		dict
		"""

		uri = self.client.uri("Project", "License")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data

		licenses = {}
		for entry in data:
			licenses[entry["displayName"]] = entry
		return licenses

###############################################################################

	def resource_types(self) -> dict:
		"""
		Retrieves a list of the available resource types in Coscine.

		Returns
		-------
		dict
		"""

		uri = self.client.uri("Resources", "ResourceType", "types")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data

		types = {}
		for it in data:
			if it["isEnabled"]:
				types[it["displayName"]] = it
		return types

###############################################################################

	def application_profiles(self) -> dict:
		"""
		Queries the list of available application profiles in Coscine.

		Returns
		--------
		dict
			A dictionary containing the application profile names as keys.
		"""

		uri = self.client.uri("Metadata", "Metadata", "profiles")
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data

		profiles = {}
		for entry in data:
			name = urllib.parse.urlparse(entry)[2]
			name = os.path.relpath(name, "/coscine/ap/")
			name = name.upper()
			profiles[name] = entry
		return profiles

###############################################################################

	@staticmethod
	def _parse_application_profile(profile: dict) -> dict:
		"""
		Parses an application profile into an easier to access dictionary by
		altering the key naming. It should increase readability both of the
		application profile itself and the code accessing/modifying it.

		Parameters
		-----------
		profile : dict
			The application profile to parse as a dictionary. Retrieved by
			e.g. StaticServer.application_profile(...).

		Returns
		-------
		dict
			The modified/parsed application profile as a dictionary
		"""

		def _get_lang(entry, lang):
			for it in entry:
				if it["@language"] == lang:
					return it
			return None

		# This function is absolutely cursed, isn't it? :^)
		# Don't stare at it for too long, or it may haunt you in your dreams.

		W3PREFIX = "http://www.w3.org/ns/shacl#%s"
		data = {}
		profile = profile[0]
		data["id"] = profile["@id"]
		graph = []
		for entry in profile["@graph"]:
			obj = {}
			if W3PREFIX % "name" not in entry:
				continue
			obj["id"] = entry["@id"]
			obj["path"] = entry[W3PREFIX % "path"][0]["@id"]
			obj["order"] = int(entry[W3PREFIX % "order"][0]["@value"])
			if W3PREFIX % "minCount" in entry:
				obj["minCount"] = int(entry[W3PREFIX % "minCount"][0]["@value"])
			if W3PREFIX % "maxCount" in entry:
				obj["maxCount"] = int(entry[W3PREFIX % "maxCount"][0]["@value"])
			obj["name"] = {
				"de": _get_lang(entry[W3PREFIX % "name"], "de")["@value"],
				"en": _get_lang(entry[W3PREFIX % "name"], "en")["@value"]
			}
			if W3PREFIX % "datatype" in entry:
				obj["datatype"] = entry[W3PREFIX % "datatype"][0]["@id"]
				obj["type"] = "literal"
			if W3PREFIX % "class" in entry:
				obj["class"] = entry[W3PREFIX % "class"][0]["@id"]
				obj["datatype"] = obj["class"]
				obj["type"] = "uri"
			graph.append(obj)
		data["graph"] = graph
		return data

###############################################################################

	def application_profile(self, path: str, id: str = None,
								parse: bool = False) -> dict:
		"""
		Retrieves a specific application profile.

		Parameters
		-----------
		path : str
			Path/Url to the application profile.
			(e.g. Resource.data["applicationProfile"]))
		id : str, default: None
			Coscine resource ID.
		parse : bool
			Specifies wether the application profile should be parsed with
			self._parse_application_profile(...) before returning.
		
		Returns
		-------
		dict
			An application profile as a dictionary.
		"""

		uri = self.client.uri("Metadata", "Metadata", "profiles", path, id)
		if uri in self.cache:
			profile = self.cache[uri]
		else:
			profile = self.client.get(uri).json()
			self.cache[uri] = profile

		if parse:
			profile = self._parse_application_profile(profile)
		return profile

###############################################################################

	def instance(self, id: str, link: str) -> dict:
		"""
		Returns a static project instance

		Parameters
		----------
		id : str
			Coscine project id.
		link : str
			uri to query.
		

		Returns
		-------
		dict
			instance
		"""

		uri = self.client.uri("Metadata", "Metadata", "instances", id, link)
		if uri in self.cache:
			data = self.cache[uri]
		else:
			data = self.client.get(uri).json()
			self.cache[uri] = data
		
		return data

###############################################################################