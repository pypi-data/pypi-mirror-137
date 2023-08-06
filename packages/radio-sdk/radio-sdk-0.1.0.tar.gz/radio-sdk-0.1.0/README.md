# Radio Browser SDK

This is an SDK for the Radio Browser API.

API Keys can be aquired from signing up to RapidAPI and subscribing to this (free) API here: [rapidapi](https://rapidapi.com/phranck/api/radio-browser/)

radio_sdk can be installed with

```
    pip install radio_sdk
```

radio_sdk can be initialized with 

```
    # Please remember to aquire api_key from rapidapi radio browser page.
    api_key = ""
    radio = radio_sdk(api_key)
```

radio_sdk then has 15 functions has their own parameters to gather data.

## list of country codes

```
    format = "json" || "csv || "xml"
    order = "name" || "stationcount"
    reverse = "true" || "false"
    hidebroken = "true" || "false"

    out = radio.list_of_country_codes(format, order, reverse, hidebroken)

    print(out)
```

## list of codecs

```
    format = "json" || "csv || "xml"
    order = "name" || "stationcount"
    reverse = "true" || "false"
    hidebroken = "true" || "false"

    out = radio.list_of_codecs(format, order, reverse, hidebroken)

    print(out)
```

## list of states

```
    # parameters
    format = "json" || "csv || "xml"
    order = "name" || "stationcount"
    reverse = "true" || "false"
    hidebroken = "true" || "false"

    # declaration
    out = radio.list_of_states(format, order, reverse, hidebroken)

    # print
    print(out)
```

## list of languages

```
    # parameters
    format = "json" || "csv || "xml"

    # declaration
    out = radio.list_of_languages(format)

    # print
    print(out)
```

## list of tags

```
    # parameters
    format = "json" || "csv || "xml"

    # declaration
    out = radio.list_of_tags(format)

    # print
    print(out)
```

## list of stations

```
    # parameters
    format = "json" || "csv || "xml"
    order = "name" || "stationcount"
    reverse = "true" || "false"
    hidebroken = "true" || "false"
    offset = "0"
    limit = "100" to "100000"

    # declaration
    out = radio.list_of_radio_stations(format, order, reverse, offset, limit, hidebroken)

    # print
    print(out)
```

## list of all radio stations

```
    # parameters
    format = "json" || "csv || "xml"
    order = "name" || "stationcount"
    reverse = "true" || "false"
    hidebroken = "true" || "false"
    offset = "0"
    limit = "100" to "100000"

    # declaration
    out = radio.list_of_all_radio_stations(format, order, reverse, offset, limit, hidebroken)

    # print
    print(out)
```

## list of station clicks

```
    # parameters
    format = "json" || "csv || "xml"
    stationuuid = ""
    seconds = "0"

    # declaration
    out = radio.list_of_station_clicks(format, stationuuid, seconds)

    # print
    print(out)
```

## search radio stations by uuid

```
    # parameters
    format = "json" || "csv || "xml"
    uuid = ""

    # declaration
    out = radio.search_radio_stations_by_uuid(format, uuid)

    # print
    print(out)
```

## search radio stations by url

```
    # parameters
    format = "json" || "csv || "xml"
    url = ""

    # declaration
    out = radio.search_radio_stations_by_uuid(format, url)

    # print
    print(out)
```

## search radio stations by url

```
    # parameters
    format = "json" || "csv || "xml"
    offset = "0"
    limit = "100000"
    hidebroken = "true"

    # declaration
    out = radio.stations_by_clicks(format, offset, limit, hidebroken)

    # print
    print(out)
```

## stations by votes

```
    # parameters
    format = "json" || "csv || "xml"
    offset = "0"
    limit = "100000"
    hidebroken = "true"

    # declaration
    out = radio.stations_by_votes(format, offset, limit, hidebroken)

    # print
    print(out)
```

## station by last click

```
    # parameters
    format = "json" || "csv || "xml"
    offset = "0"
    limit = "100000"
    hidebroken = "true"

    # declaration
    out = radio.station_by_last_click(format, offset, limit, hidebroken)

    # print
    print(out)
```

## vote for a station

```
    # parameters
    format = "json" || "csv || "xml"
    uuid = ""

    # declaration
    out = radio.vote_for_a_station(format, uuid)

    # print
    print(out)
```

### Thanks and happy developing/ listening!




