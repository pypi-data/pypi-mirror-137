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
"""
Coscine Python SDK

This python3.x package provides an SDK for interfacing with Coscine.
It is maintained and developed by the community and should not be regarded
as an official service of RWTH Aachen.
You can use the package to integrate Coscine in your python applications
and easily:
- create, edit or delete projects and resources
- invite and manage project members
- upload and download files, resources and projects
- manage your metadata
"""
###############################################################################

from .client import Client
from .project import Project, ProjectForm, ProjectMember
from .resource import Resource, ResourceForm
from .object import Object
from .metadata import MetadataForm, MetadataPresetForm
from .exceptions import *