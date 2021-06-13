# spotify-backup ![CI](https://github.com/emkor/spotify-backup/workflows/CI/badge.svg)
Fork of [caseychu/spotify-backup](https://github.com/caseychu/spotify-backup)

Python CLI tool that exports all of your Spotify playlists and/or liked songs into CSV file

## installation
- pre-requisites: Python >=3.7, pip
- command to install: `pip install spotify-backup` (dependency-free)

## usage
- get your Spotify OAuth Token [here](https://developer.spotify.com/web-api/console/get-playlists/)
- execute `spotify-backup <OUTPUT FILE> --dump playlists,liked --token <YOUR TOKEN>`
    - example: `spotify-backup my_backup.csv --dump playlists,liked --token SOME_VERY_LONG_TOKEN`

## output format
`<PLAYLIST NAME>,<TRACK URI>,<COMMA-SEPARATED TRACK ARTISTS>,<ALBUM NAME>,<TRACK NAME>`

## output example
```csv
Liked Songs,spotify:track:7eMlLQXY5QICXuafv4haUg,"Massive Attack, Azekel",Ritual Spirit,Ritual Spirit
Liked Songs,spotify:track:53Zvj4xbSFKwSJeXjyocHK,Boy Harsher,Careful,Fate
Liked Songs,spotify:track:1IP0wkv3Hj7cPE159G9c2O,"PRO8L3M, Brodka",Fight Club,Żar
test,spotify:track:4u3cJaAUcmp4qPKUUcxXZv,UNKLE,War Stories,Mistress (feat Alicia Temple)
test,spotify:track:0MabrxpL9vrCJeOjGMnGgM,"Perturbator, Greta Link",The Uncanny Valley,Venger (feat. Greta Link)
test,spotify:track:0FoR0PrLkw6t64waJX3qT5,"Brodka, A_GIM",Wszystko czego dziś chcę (z serialu Rojst na Showmax),Wszystko czego dziś chcę (z serialu Rojst na Showmax)
test,spotify:track:5b2ACxzxhGeLPDr500fQzy,"deadmau5, Rob Swire",Ghosts 'n' Stuff,Ghosts 'N' Stuff - Radio Edit
test,spotify:track:4oezx4rQJnIBpKurukB2gN,trentemøller,Moan,Moan - Trentemøller Remix - Radio Edit
test,spotify:track:1itVstaGVBLPXqlv50HvDn,Goldfrapp,Ride A White Horse,Ride a White Horse - Serge Santiágo Re-Edit
```

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
- tool downloads everything into memory before writing to file, need to rewrite client and use streaming / generators
