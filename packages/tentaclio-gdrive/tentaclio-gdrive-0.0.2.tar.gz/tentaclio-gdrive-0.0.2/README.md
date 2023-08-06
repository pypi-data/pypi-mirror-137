
# tentaclio-gdrive

A package containing all the dependencies for the gdrive tentaclio schema .

## Quick Start

This project comes with a `Makefile` which is ready to do basic common tasks

```
$ make help
install                       Initalise the virtual env installing deps
clean                         Remove all the unwanted clutter
lock                          Lock dependencies
update                        Update dependencies (whole tree)
sync                          Install dependencies as per the lock file
lint                          Lint files with flake and mypy
format                        Run black and isort
test                          Run unit tests
circleci                      Validate circleci configuration (needs circleci cli)
```


## Configuring access to google drive.
Google drive support is _experimental_ and should be used at your own risk. Also, due to google drive itself it's rather slow.

1. Get the credentials.
First we need a credentials file in order to be able to generate tokens. The easiest way to do this is by going to [this example](https://developers.google.com/drive/api/v3/quickstart/python),
click on enable drive api. Give the project a name of your choosing (eg `tentaclio`). Click on `APIs and services` -> `Credentials` -> `Create credentials` -> Create OAuth client ID`, select `Desktop app` and `Download JSON`

2. Generate token file

```
pipenv install tentaclio && \
    pipenv run python -m tentaclio_gdrive google-token generate --credentials-file ~/Downloads/credentials.json
```
This will open a browser with a google auth page, log in and accept the authorisation request.
The token file has been saved in a default location '~/.tentaclio_google_drive.json'. You can also configure this via the env variable `TENTACLIO__GOOGLE_DRIVE_TOKEN_FILE`

3. Get rid of credentials.json
The `credentials.json` file is no longer need, feel free to delete it.
