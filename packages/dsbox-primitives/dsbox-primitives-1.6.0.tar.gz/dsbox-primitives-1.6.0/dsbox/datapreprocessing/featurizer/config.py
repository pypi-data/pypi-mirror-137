import os
from d3m import utils

try:
    import d3m.__init__ as d3m_info
    D3M_API_VERSION = d3m_info.__version__
except Exception:
    D3M_API_VERSION = '2021.12.19'

VERSION = "1.6.0"

REPOSITORY = "https://gitlab.com/datadrivendiscovery/contrib/dsbox-primitives.git"
PACAKGE_NAME = "dsbox-primitives"

D3M_PERFORMER_TEAM = 'ISI'
D3M_CONTACT = "mailto:kyao@isi.edu"


INSTALLATION_TYPE = 'PYPI'
if INSTALLATION_TYPE == 'PYPI':
    INSTALLATION = {
        "type" : "PIP",
        "package": PACAKGE_NAME,
        "version": VERSION
    }
else:
    # INSTALLATION_TYPE == 'GIT'
    TAG_NAME = "{git_commit}".format(git_commit=utils.current_git_commit(os.path.dirname(__file__)), )
    PACKAGE_URI = "git+" + REPOSITORY + "@" + TAG_NAME + "#egg=" + PACAKGE_NAME

    INSTALLATION = {
        "type" : "PIP",
        "package_uri": PACKAGE_URI,
    }
