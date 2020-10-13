'''This file stores templates for all the different Google Fit DataSources
Each type of data uploaded to Google Fit requires a matching datasource,
if iFit will open their API it should be possible to get the treadmill make and model
and replace the fixed ones here, you can change the make and model here manually until
that is done'''
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
    {
        "datasourceid": "raw:com.google.location.sample:"
        + ProjectNumber
        + ":NordicTrack:Commercial2950:100001",
        "type": "raw",
        "application": {"name": "ifitsync"},
        "dataType": {"name": "com.google.location.sample"},
        "device": {
            "type": "unknown",
            "manufacturer": "NordicTrack",
            "model": "Commercial2950",
            "uid": "100001",
            "version": "1.0",
        },
    },
    {
  "datasourceid": "raw:com.ifitsync.treadmillincline.degrees:"
  + ProjectNumber
  + ":TreadmillIncline",
  "dataStreamName": "TreadmillIncline",
  "type": "raw",
  "application": {
    "detailsUrl": "https://github.com/omriasta/ifitsync",
    "name": "Treadmill Incline Degrees",
    "version": "1"
  },
  "dataType": {
    "name": "com.ifitsync.treadmillincline.degrees",
    "field": [
     {
      "name": "treadmill_incline_degrees",
      "format": "floatPoint"
     }
    ]
   }
    },
    {
  "datasourceid": "raw:com.ifitsync.treadmill.elevation:"
  + ProjectNumber
  + ":TreadmillElevation",
  "dataStreamName": "TreadmillElevation",
  "type": "raw",
  "application": {
    "detailsUrl": "https://github.com/omriasta/ifitsync",
    "name": "Treadmill Elevation Meters",
    "version": "1"
  },
  "dataType": {
    "name": "com.ifitsync.treadmill.elevation",
    "field": [
     {
      "name": "treadmill_elevation_meters",
      "format": "floatPoint"
     }
    ]
   }
    }
]

