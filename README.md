# spotify-backup
Fork of [caseychu/spotify-backup](https://github.com/caseychu/spotify-backup)

A Python CLI tool that exports all of your Spotify playlists and/or liked songs

## installation
- pre-requisites: Python >=3.7, pip
- command to install: `pip install spotify-backup`
- TODO not published yet

## usage
TODO

## options
```
usage: spotify-backup [-h] [--token TOKEN] --dump {liked,playlists,playlists,liked,playlists,liked} [-d] file

Exports your Spotify playlists and/or Liked songs to CSV file.

positional arguments:
  file                  output filename

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Spotify OAuth token; requires `playlist-read-private` and `user-library-read` scopes; to get it, visit
                        https://developer.spotify.com/console/get-playlists/ may also use SPOTIFY_OAUTH_TOKEN env var
  --dump {liked,playlists,playlists,liked,playlists,liked}
                        dump playlists or liked songs, or both (default: playlists)
  -d, --debug           Enable more verbose logging
```

## known issues
- collaborative playlists and playlist folders don't show up in the API, sadly.
- tool downloads everything into memory, need to rewrite client in streaming manner