import os
import d3m
from d3m import utils

D3M_API_VERSION = "2021.12.19" #d3m.__version__
VERSION = "1.1.0"

REPOSITORY = "https://github.com/brekelma/dsbox_corex"
PACAKGE_NAME = "dsbox-corex"

D3M_PERFORMER_TEAM = 'ISI'


INSTALLATION_TYPE = 'PYPI'
if INSTALLATION_TYPE == 'PYPI':
    INSTALLATION = {
        "type" : "PIP",
        "package": PACAKGE_NAME,
        "version": VERSION
    }
else:
    TAG_NAME = "{git_commit}".format(git_commit=utils.current_git_commit(os.path.dirname(__file__)), )
    PACKAGE_URI_COREX = "git+" + REPOSITORY + "@" + TAG_NAME + "#egg=" + PACAKGE_NAME

    INSTALLATION = {
        "type" : "PIP",
        "package_uri": PACKAGE_URI_COREX,
    }
