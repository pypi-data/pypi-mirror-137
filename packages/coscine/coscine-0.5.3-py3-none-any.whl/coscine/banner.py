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
# This file contains a printable banner. It is printed to stdout
# upon initialization of the SDK with verbose mode enabled.
# The banner includes the current package version and title. Otherwise
# it serves no special purpose and can be disregarded for anything other
# than demonstrations.
###############################################################################

from .version import __version__

###############################################################################

BANNER = \
"""
                     _             
                    (_)            
   ___ ___  ___  ___ _ _ __   ___  
  / __/ _ \/ __|/ __| | '_ \ / _ \ 
 | (_| (_) \__ \ (__| | | | |  __/ 
  \___\___/|___/\___|_|_| |_|\___| 
____________________________________

    Coscine Python SDK %s
____________________________________
""" % __version__

###############################################################################