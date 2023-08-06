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

from collections.abc import MutableMapping
from .exceptions import *
from typing import List
import prettytable

###############################################################################

class InputForm(MutableMapping):

	"""
	The InputForm class provides an overarching input form interface for
	metadata, project or resource editing. It is meant to resemble
	the input form of the web interface as closely as possible.
	The input form is built opon the python dict datatype and can be interacted
	with like with any other dictionary. However some additional functions
	are provided, to make it easier to interact with the form and its contents.
	"""

	# Form flags
	NONE = 0
	REQUIRED = 1
	CONTROLLED = 2
	SET = 4
	FIXED = 8
	LIST = 16
	SPECIAL = 32

###############################################################################

	def __init__(self, name: str, lang: str, entries: list, vocabulary: dict):

		"""
		Each form is intialized with a name, a language present and the actual
		entries and their vocabularies.

		Parameters
		-----------
		name : str
			The name of the form (e.g. 'Resource Form').
		lang : str
			The language of the client ('en' or 'de').
		entries : list
			A list of form entries (list of dict).
		vocabulary : dict
			A mapping of form field key to vocabulary dict.
		"""

		self._name = name
		self._lang = lang
		self._entries = entries
		self._keys = {}
		for entry in entries:
			self._keys[entry["name"][self._lang]] = entry
		self._vocabulary = vocabulary
		self.store = {}

###############################################################################

	def __getitem__(self, key: str) -> dict:
		if key not in self.keys():
			raise KeyError(key)
		elif key in self.store:
			return self.store[key]
		else:
			return None

###############################################################################

	def __setitem__(self, key: str, value: object):
		if key not in self._keys:
			raise KeyError("Key `%s` not expected by form." % key)
		if self._expects_list(key) and (type(value) is not list):
			raise ValueError("Expected a list value for key `%s`." % key)
		if self.is_controlled(key):
			vocabulary = self.get_vocabulary(key)
			if type(value) is list:
				self.store[key] = []
				for val in value:
					if val in vocabulary:
						self.store[key].append(val)
					else:
						raise VocabularyError(val)
			else:
				if value in vocabulary:
					self.store[key] = value
				else:
					raise VocabularyError(value)
		else:
			self.store[key] = value

###############################################################################

	def __delitem__(self, key: str):
		del self.store[key]

###############################################################################

	def __iter__(self):
		return iter(self.store)

###############################################################################

	def __len__(self):
		return len(self.store)

###############################################################################

	def __str__(self) -> str:
		table = prettytable.PrettyTable(("R", "C", "Field", "Value"))
		table.max_width["Value"] = 40
		rows = []
		for key in self.keys():
			flag1 = flag2 = " "
			if self.is_required(key):
				flag1 = "X"
			if self.is_controlled(key):
				flag2 = "X"
			if key in self.store:
				value = self.store[key]
			else:
				value = ""
			rows.append((flag1, flag2, key, value))
		table.add_rows(rows)
		return table.get_string(title=self._name)

###############################################################################

	def __repr__(self) -> str:
		return self.__str__()

###############################################################################

	def _expects_list(self, key: str) -> bool:
		"""
		Returns wether the field referenced by key requires a list.
		"""

		return self._keys[key]["flags"] & self.LIST

###############################################################################

	def is_required(self, key: str) -> bool:

		"""
		Determines wether the given key is a required field.

		Parameters
		-----------
		key : str
			A key contained in the input form (e.g. 'Author').

		Returns
		-------
		True
			If key is a required field.
		False
			If key is not a required field.
		"""

		return self._keys[key]["flags"] & self.REQUIRED

###############################################################################

	def is_controlled(self, key: str) -> bool:

		"""
		Determines wether the given key is a controlled field. Controlled
		fields have a vocabulary. Any value assigned to the key must be
		contained in that vocabulary.

		Parameters
		-----------
		key : str
			A key contained in the input form (e.g. 'Author')

		Returns
		-------
		True
			If key is a controlled field.
		False
			If key is not a controlled field.
		"""

		return self._keys[key]["flags"] & self.CONTROLLED

###############################################################################

	def get_field(self, key: str) -> str:

		"""
		Returns the internal field name of a field contained in the form.

		Parameters
		-----------
		key : str
			A key contained in the input form (e.g. 'Author').

		Returns
		-------
		A string with the name used to represent the field internally in
		Coscine JSON-LD. (e.g. 'doe' instead of 'John Doe')
		"""

		return self._keys[key]["field"]

###############################################################################

	def get_vocabulary(self, key: str) -> dict:

		"""
		Returns the vocabulary of a controlled field. Uncontrolled fields
		result in an exception.

		Parameters
		----------
		key : str
			Any field contained inside of the form

		Returns
		--------
		dict
			The vocabulary of the form field.
		"""

		if self.is_controlled(key):
			return self._vocabulary[self.get_field(key)]
		else:
			msg = "Key [%s] is not controlled by a vocabulary!" % key
			raise CoscineException(msg)

###############################################################################

	def keys(self) -> List[str]:

		"""
		Returns a list of all keys contained within the input form.

		Returns
		-------
		list[str]
		"""

		return self._keys.keys()

###############################################################################

	def reset(self):

		"""
		Resets the input form to default values.
		"""

		self.store.clear()

###############################################################################

	def parse(self, data: dict):
		pass

###############################################################################

	def generate(self):
		pass

###############################################################################

	def entry(self, field: str) -> dict:

		"""
		Returns an entry of the input form. An entry resembles the internal
		representation of a form field.

		Parameters
		----------
		field : str
			The Coscine internal name of the field (see InputForm.get_field(...)).

		Returns
		-------
		dict
			The fields internal entry representation as a dict.
		"""

		for item in self._entries:
			if item["field"] == field:
				return item
		return None

###############################################################################