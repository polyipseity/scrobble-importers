from typing import NewType

StrURL = NewType("StrURL", str)
StrUUID = NewType("StrUUID", str)
StrVersion = NewType("StrVersion", str)
Timestamp = NewType("Timestamp", int)

NAME = "scrobble-importers"
VERSION = StrVersion("1.0.0")

LB_MAX_LISTENS_PER_REQUEST = 1000  # <https://listenbrainz.readthedocs.io/latest/users/api/core.html#listenbrainz.webserver.views.api_tools.MAX_LISTENS_PER_REQUEST>
