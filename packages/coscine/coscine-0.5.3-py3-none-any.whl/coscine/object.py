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
from typing import TYPE_CHECKING, Callable, List, Type
if TYPE_CHECKING:
	from .client import Client
	from .resource import Resource
import os
import json
from .progressbar import ProgressBar
from .metadata import MetadataForm

###############################################################################

class Object:
	"""
	Objects in Coscine represent file-like data. We could have called it
	File, but in case of linked data we are not actually dealing with files
	themselves, but with links to files. As such, we require a more general
	datatype.
	"""

	client: Client
	resource: Resource
	data: dict
	name: str
	size: int
	type: str
	path: str
	is_folder: bool

	CHUNK_SIZE: int = 4096

###############################################################################

	def __init__(self, resource: Resource, data: dict) -> None:
		"""
		Initializes the Coscine object.

		Parameters
		----------
		resource : coscine.Resource
			Coscine resource handle.
		data : dict
			data of the file-like object.
		"""

		self.client = resource.client
		self.resource = resource
		self.data = data
		self.name = data["Name"]
		self.size = data["Size"]
		self.type = data["Kind"]
		self.path = data["Path"]
		self.is_folder = data["IsFolder"]

###############################################################################

	def __repr__(self) -> str:
		return self.__str__()

###############################################################################

	def __str__(self) -> str:
		return json.dumps(self.data, indent=4)

###############################################################################

	def metadata(self) -> dict:
		"""
		Retrieves the metadata of the file-like object.

		Returns
		-------
		dict
			Metadata as a python dictionary.
		None
			If no metadata has been set for the file-like object.
		"""

		uri = self.client.uri("Tree", "Tree", self.resource.id)
		args = {"path": self.path}
		data = self.client.get(uri, params=args).json()
		metadata = data["data"]["metadataStorage"]
		if not metadata:
			return None
		metadata = metadata[0]
		for key in metadata:
			return metadata[key]

###############################################################################

	def content(self) -> bytes:
		"""
		Retrieves the content/data of the object. In case of linked data
		this would be the link, not the actual file itself. It is impossible
		to get the file contents of linked data objects with this python module.
		In case of rds or rds-s3 data this would return the file contents.
		Be aware that for very large files this will consume a considerable
		amount of RAM memory!

		Returns
		-------
		bytes
			A raw byte-array containing the Coscine file-object's data.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		return self.client.get(uri, params = args).content

###############################################################################

	def download(self, path: str = "./", callback: Callable[[int]] = None) -> None:
		"""
		Downloads the file-like object to the local harddrive.

		Parameters
		----------
		path : str, default: "./"
			The path to the download location on the harddrive.
		callback : function(chunksize: int)
			A callback function to be called during downloading chunks.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		response = self.client.get(uri, params = args, stream = True)
		path = os.path.join(path, self.name)
		fd = open(path, "wb")
		bar = ProgressBar(self.client, self.size, self.name, "DOWN", callback)
		for chunk in response.iter_content(chunk_size = self.CHUNK_SIZE):
			fd.write(chunk)
			bar.update(len(chunk))
		fd.close()

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the file-like object on the Coscine server.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		self.client.delete(uri, params = args)

###############################################################################

	def update(self, metadata) -> None:
		"""
		Updates the metadata of the file-like object.

		Parameters
		----------
		metadata : coscine.MetadataForm or dict
			MetadataForm or JSON-LD formatted metadata dict
		
		Raises
		------
		TypeError
			If argument `metadata` has an unexpected type.
		"""

		if type(metadata) is MetadataForm:
			metadata = metadata.generate()
		elif type(metadata) is not dict:
			raise TypeError("Expected MetadataForm or dict.")
		
		uri = self.client.uri("Tree", "Tree", self.resource.id)
		args = {"path": self.path}
		self.client.put(uri, params = args, data = metadata)

###############################################################################

	def form(self) -> MetadataForm:
		"""
		Returns a MetadataForm filled with the metadata of the file-like object
		"""

		form = MetadataForm(self.resource)
		form.parse(self.metadata())
		return form

###############################################################################

	def objects(self, **kwargs) -> List[Object]:
		if self.is_folder:
			return self.resource.objects(path=self.path, **kwargs)
		else:
			raise TypeError("object is not a directory!")

###############################################################################

	def object(self, displayName: str = None, **kwargs) -> Object:
		if self.is_folder:
			if displayName.endswith("/"): # expect directory
				displayName = self.name + "/" + displayName
			return self.resource.object(displayName = displayName,
											path=self.path, **kwargs)
		else:
			raise TypeError("object is not a directory!")

###############################################################################