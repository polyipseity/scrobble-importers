from typing import NewType

StrURL = NewType("StrURL", str)
StrUUID = NewType("StrUUID", str)
StrVersion = NewType("StrVersion", str)
Timestamp = NewType("Timestamp", int)

NAME = "scrobble-importers"
VERSION = StrVersion("1.0.0")
