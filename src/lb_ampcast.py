from _init import NAME, StrURL, StrUUID, StrVersion, Timestamp, VERSION
from itertools import batched
from json import load
from pylistenbrainz import Listen, ListenBrainz  # type: ignore
from tldextract import extract
from typing import NotRequired, Sequence, TypedDict, final

LB_MAX_LISTENS_PER_REQUEST = 1000  # <https://listenbrainz.readthedocs.io/latest/users/api/core.html#listenbrainz.webserver.views.api_tools.MAX_LISTENS_PER_REQUEST>
METADATA_PLAYER = "ampcast"


@final
class AmpcastSettings:
    @final
    class Root(TypedDict):
        ampcastVersion: StrVersion
        backup: "AmpcastSettings.Backup"

    @final
    class Backup(TypedDict):
        listens: NotRequired[Sequence["AmpcastSettings.Listen"]]

    @final
    class Listen(TypedDict):
        itemType: int
        mediaType: int
        playbackType: int
        src: str
        externalUrl: StrURL
        title: str
        aspectRatio: float
        duration: float
        thumbnails: Sequence["AmpcastSettings.Thumbnail"]
        owner: "AmpcastSettings.Owner"
        playedAt: Timestamp
        album: str
        artists: Sequence[str]
        recording_mbid: StrUUID
        artist_mbids: Sequence[StrUUID]
        caa_mbid: StrUUID
        sessionId: str
        lastfmScrobbledAt: Timestamp
        listenbrainzScrobbledAt: Timestamp

    @final
    class Thumbnail(TypedDict):
        url: StrURL
        width: int
        height: int

    @final
    class Owner(TypedDict):
        name: str
        url: StrURL


def main():
    token = input("token: ")
    lb_client = ListenBrainz()
    lb_client.set_auth_token(token, check_validity=True)  # type: ignore

    settings = input("settings: ")
    with open(settings, mode="rt", encoding="UTF-8") as settings_file:
        settings_json: AmpcastSettings.Root = load(settings_file)
    player_version = settings_json["ampcastVersion"]
    listens = settings_json["backup"].get("listens", ())

    for listen_batch in batched(listens, LB_MAX_LISTENS_PER_REQUEST):
        lb_listen_batch = tuple(
            Listen(
                track_name=listen["title"],
                artist_name=listen["artists"][0],
                listened_at=listen["playedAt"],
                release_name=listen["album"],
                recording_mbid=listen["recording_mbid"],
                artist_mbids=listen["artist_mbids"],
                release_mbid=listen["caa_mbid"],
                tags=None,
                release_group_mbid=None,
                work_mbids=None,
                tracknumber=None,
                spotify_id=None,
                listening_from=METADATA_PLAYER,
                isrc=None,
                additional_info={
                    "media_player": METADATA_PLAYER,
                    "media_player_version": player_version,
                    "submission_client": NAME,
                    "submission_client_version": VERSION,
                    "music_service": extract(listen["externalUrl"]).registered_domain,
                    # "music_service_name": None,
                    "origin_url": listen["externalUrl"],
                    "duration_ms": int(listen["duration"] * 1000),
                },
                username=None,
            )
            for listen in listen_batch
        )
        lb_client.submit_multiple_listens(lb_listen_batch)  # type: ignore


if __name__ == "__main__":
    main()
