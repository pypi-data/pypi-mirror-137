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

###############################################################################
# This file defines exceptions used by the Coscine python SDK.
# The base exception class is called CoscineException. It directly inherits
# its properties from the standard python Exception class.
# Although never used directly it provides the basis for more specific
# exceptions, thus allowing you to catch any Coscine exception with one
# except statement.
###############################################################################

class CoscineException(Exception):
	"""
	Coscine base Exception class.
	"""
	pass

###############################################################################

class ConnectionError(CoscineException):
	"""
	In case the client is not able to establish a connection with
	the Coscine servers, a ConnectionError is raised.
	"""
	pass

###############################################################################

class ClientError(CoscineException):
	"""
	An error has been made or detected on the client side.
	"""
	pass

###############################################################################

class ServerError(CoscineException):
	"""
	An error has been made or detected on the Coscine server.
	"""
	pass

###############################################################################

class VocabularyError(CoscineException):
	"""
	Raised in InputForms when a supplied value is not contained within
	a controlled vocabulary.
	"""
	pass

###############################################################################

class RequirementError(CoscineException):
	"""
	Commonly raised in InputForms when a required field has not been set.
	"""
	pass

###############################################################################

class AuthorizationError(CoscineException):
	"""
	AuthorizationErrors are thrown when the owner of the Coscine API
	token does not hold enough privileges.
	"""
	pass

###############################################################################

class AmbiguityError(CoscineException):
	"""
	An AmbiguityError is raised in cases where two objects could
	not be differentiated between.
	"""
	pass

###############################################################################

class ParameterError(CoscineException):
	"""
	Invalid (number of) function parameters provided. In some cases
	the user has the option of choosing between several optional arguments,
	but has to provide at least one.
	"""
	pass

###############################################################################