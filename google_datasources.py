import json

with open("credentials.json") as credentials:
    credentials = json.load(credentials)

ProjectNumber = credentials.get("installed").get("client_id").split("-")[0]

GOOGLE_DATA_SOURCES = [
    {
        "datasourceid": "raw:com.google.heart_rate.bpm:"
        + ProjectNumber
        + ":NordicTrack:IFHRM214:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.heart_rate.bpm",
            "field": [{"format": "floatPoint", "name": "bpm"}],
        },
        "device": {
            "type": "chestStrap",
            "manufacturer": "NordicTrack",
            "model": "IFHRM214",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.speed:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.speed",
            "field": [{"format": "floatPoint", "name": "speed"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.power.sample:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.power.sample",
            "field": [{"format": "floatPoint", "name": "watts"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.calories.expended:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.calories.expended",
            "field": [{"format": "floatPoint", "name": "calories"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.distance.delta:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.distance.delta",
            "field": [{"format": "floatPoint", "name": "distance"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.step_count.delta:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.step_count.delta",
            "field": [{"format": "integer", "name": "steps"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
        "datasourceid": "raw:com.google.activity.segment:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {
            "name": "com.google.activity.segment",
            "field": [{"format": "integer", "name": "activity"}],
        },
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
]

