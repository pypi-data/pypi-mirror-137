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
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
	from .client import Client
import tqdm

###############################################################################

class ProgressBar:
	"""
	The ProgressBar class is a simple wrapper around tqdm
	progress bars. It is used in download/upload methods and provides the
	benefit of remembering state information and printing only when in
	verbose mode.

	Attributes
	----------
	client : coscine.Client
		Coscine Python SDK client handle.
	bar : tqdm.tqdm
		tqdm Progress Bar instance.
	n : int
		Number of bytes read.
	callback : Callable[int]
		Callback function to call on update.
	"""

	client: Client
	bar: tqdm.tqdm
	n: int
	callback: Callable[[int]]

	def __init__(self, client: Client, filesize: int, key: str, \
				mode: str, callback: Callable[[int]] = None) -> None:
		"""
		Initializes a state-aware tqdm ProgressBar.

		client : coscine.Client
			Coscine python SDK client handle
		filesize : int
			Size of the file object in bytes
		key : str
			key/filename of the file object
		mode : str
			'UP' or 'DOWN' referring to upload and download
		callafter : function(chunksize: int)
			 callback function to call after each update
		"""

		MODES = {
			"UP":	"↑",
			"DOWN":	"↓"
		}

		if mode not in MODES:
			raise ValueError("Invalid value for argument 'mode'! "\
					"Possible values are %s." % str(MODES.keys()))
		
		self.client = client
		self.callback = callback
		self.n = 0
		if self.client.verbose:
			self.bar = tqdm.tqdm(total=filesize, unit="B", unit_scale=True,\
										desc="%s %s" % (MODES[mode], key))

###############################################################################

	def update(self, chunksize: int) -> None:
		"""
		Updates the progress bar with respect to the consumed chunksize.
		If a callafter function has been provided to the Constructor, it is
		called during the update.

		Parameters
		----------
		chunksize : int
			indicates the amount of bytes consumed since the last update
		"""

		self.n += chunksize
		if self.client.verbose:
			self.bar.update(chunksize)
		if self.callback:
			self.callback(chunksize)

###############################################################################