import argparse
import csv
import logging
import os
import sys
import typing as t

from spotify_backup.client import SpotifyAPI

OAUTH_TOKEN_ENV_VAR = "SPOTIFY_OAUTH_TOKEN"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exports your Spotify playlists and/or Liked songs to CSV file.")
    parser.add_argument("file", help="output filename")
    parser.add_argument(
        "--token",
        type=str,
        help="Spotify OAuth token; "
        "requires `playlist-read-private` and `user-library-read` scopes; "
        "to get it, visit https://developer.spotify.com/console/get-playlists/ "
        f"may also use {OAUTH_TOKEN_ENV_VAR} env var",
    )
    parser.add_argument(
        "--dump",
        type=str,
        required=True,
        default="playlists",
        choices=["liked,playlists", "playlists,liked", "playlists", "liked"],
        help="dump playlists or liked songs, or both (default: playlists)",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable more verbose logging")
    return parser.parse_args()


def _to_csv_row(
    playlist: t.Dict[str, t.Any], track: t.Dict[str, t.Any]
) -> t.Optional[t.Tuple[str, str, str, str, str]]:
    try:
        return (
            playlist["name"],
            track["track"]["uri"],
            ", ".join([artist["name"] for artist in track["track"]["artists"]]),
            track["track"]["album"]["name"],
            track["track"]["name"],
        )
    except KeyError:
        logging.warning(f"Could not translate playlist {playlist} and track {track} to CSV row, continuing")
        return None


def main():
    args = _parse_args()
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s|%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    output_file = os.path.abspath(os.path.expanduser(args.file))
    if os.path.isfile(output_file):
        logging.warning(f"Given output file {output_file} already exists!")
        sys.exit(1)

    token = args.token or os.getenv(OAUTH_TOKEN_ENV_VAR)
    if not token:
        logging.warning(f"No Spotify Oauth token set, see --help")
        sys.exit(1)

    spotify = SpotifyAPI(token)
    me = spotify.get("me")
    logging.info(f"Logged in as {me['display_name']} ({me['id']})")

    playlists = []

    # List liked songs
    if "liked" in args.dump:
        logging.info("Loading liked songs...")
        liked_tracks = spotify.list("users/{user_id}/tracks".format(user_id=me["id"]), {"limit": 50})
        playlists += [{"name": "Liked Songs", "tracks": liked_tracks}]

    # List all playlists and the tracks in each playlist
    if "playlists" in args.dump:
        logging.info("Loading playlists...")
        playlist_data = spotify.list("users/{user_id}/playlists".format(user_id=me["id"]), {"limit": 50})
        logging.info(f"Found {len(playlist_data)} playlists")

        # List all tracks in each playlist
        for playlist in playlist_data:
            logging.info("Loading playlist: {name} ({tracks[total]} songs)".format(**playlist))
            playlist["tracks"] = spotify.list(playlist["tracks"]["href"], {"limit": 100})
        playlists += playlist_data

    # Write the file.
    logging.info("Writing files...")
    with open(output_file, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for playlist in playlists:
            for track in playlist["tracks"]:
                row = _to_csv_row(playlist, track)
                if row:
                    writer.writerow(row)
    logging.info("Wrote file: " + output_file)


if __name__ == "__main__":
    main()
