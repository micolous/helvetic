# testserver

This is a test server for the Fitbit Aria API.

This probably has security weaknesses -- do not expose to the public
internet.

## Building / running with Docker (recommended)

### Building

```sh
docker build -t helvetictest .
```

### Running

You can supply environment variables to configure the app:

```sh
docker run -p 8000:8000 -e HEL_USER=michael -it helvetictest
```

This exposes an API endpoint on port 8000.

## Environment variables

The following environment variables may be used to configure the test
server:

* `HEL_NAME`: name, up to 20 characters, latin letters only

* `HEL_MIN_TOLERANCE`: minimum weight tolerance, in grams

* `HEL_MAX_TOLERANCE`: maximum weight tolerance, in grams

* `HEL_BIRTHYEAR`: your year of birth - used to calculate age

* `HEL_GENDER`: 'F' = female, 'M' = male, unset = unknown; may be used by
  scales to calculate body fat?

* 'HEL_HEIGHT`: height, in millimetres, used to calculate body fat

## Endpoints

Hitting `/` on the webserver (ie: http://localhost:8000/ ) will show the
current configuration, and recent log lines from the server.

