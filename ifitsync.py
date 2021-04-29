from get_googleaccount import main
from get_ifitaccount import FEED_JSON, HISTORY_JSON, IFIT_HIST_HEADERS
from google_datasources import GOOGLE_DATA_SOURCES
from googleapiclient.errors import HttpError
import json
import time
import requests
import math
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import os.path
from os import path

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

service = main()

'''define classes'''

class HISTORY:
    def __init__(self, JSON):
        self.id = JSON["id"]
        self.workout_id = JSON["workout_id"]
        self.duration = JSON["duration"]
        self.start_time = JSON["start"]
        self.end_time = JSON["end"]
        self.total_steps = JSON["summary"]["total_steps"]
        self.total_meters = JSON["summary"]["total_meters"]
        self.total_calories = JSON["summary"]["total_calories"]
        self.workout_json_url = "https://gateway.ifit.com/wolf-workouts-service/v1/post-workout/" + self.id + "?softwareNumber=424992&isMetric=false&locale=en-US&deviceType=tablet HTTP/1.1"
        self.workout_details_json = http.get(self.workout_json_url, headers=IFIT_HIST_HEADERS).json()
        self.title = self.workout_details_json["title"]
        self.stats_url = "https://api.ifit.com/v1/activity_logs/" + self.id
        self.stats = http.get(self.stats_url, headers=IFIT_HIST_HEADERS).json()
        self.start = self.stats["start"] * 1000000
        self.end = self.stats["end"] * 1000000
        self.lists = self.stats["stats"]
        self.type = JSON["type"]


def closest(lst, K): 
      
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lon1, lat1, *args = coord1
    lon2, lat2, *args = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))



def CheckGoogleDataSourceExists(dataSourceId):
    '''Function to check if Google DataSource Exists'''
    try:
        service.users().dataSources().get(
            userId="me", dataSourceId=dataSourceId
        ).execute()
    except HttpError as error:
        if "DataSourceId not found" in str(error):
            return False
        else:
            raise error
    else:
        return True


def CreateGoogleDataSource(GoogleDataSourceJson):
    '''Function to create a Google DataSource'''
    try:
        service.users().dataSources().create(
            userId="me", body=GoogleDataSourceJson
        ).execute()
    except HttpError as error:
        if "40" in str(error):
            raise error

    print("Datasource successfully created")


def UploadIfitHrToGoogle(IfitWorkoutJson):
    '''Function that Uploads HR data from an iFit Workout to Google'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[0]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.start
            + IfitWorkoutJson.lists["bpm"][0]["offset"] * 1000000,
            "dataTypeName": "com.google.heart_rate.bpm",
            "value": [{"fpVal": IfitWorkoutJson.lists["bpm"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson.lists["bpm"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.heart_rate.bpm",
                "value": [{"fpVal": x["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )
    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout HR data successfully")
    


def UploadIfitSpeedToGoogle(IfitWorkoutJson):
    '''Function that Uploads Speed Data from an iFit Workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[1]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.start
            + IfitWorkoutJson.lists["mps"][0]["offset"] * 1000000,
            "dataTypeName": "com.google.speed",
            "value": [{"fpVal": IfitWorkoutJson.lists["mps"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson.lists["mps"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.speed",
                "value": [{"fpVal": x["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Speed data successfully")    
    


def UploadIfitWattsToGoogle(IfitWorkoutJson):
    '''Function that Uploads Power data from an iFit workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[2]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.start
            + IfitWorkoutJson.lists["watts"][0]["offset"] * 1000000,
            "dataTypeName": "com.google.power.sample",
            "value": [{"fpVal": IfitWorkoutJson.lists["watts"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson.lists["watts"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.power.sample",
                "value": [{"fpVal": x["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Power(watts) data successfully")



def UploadIfitCaloriesToGoogle(IfitWorkoutJson):
    '''Function that Uploads Calorie data from an iFit workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[3]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.end,
            "dataTypeName": "com.google.calories.expended",
            "value": [{"fpVal": IfitWorkoutJson.stats["summary"]["total_calories"]}],
        }
    )
    '''The below section commented out as Google Fit throws data out of range for some of the points, instead uploading totals for the workout'''
    """
    for index, x in zip(
        IfitWorkoutJson["stats"]["calories"], IfitWorkoutJson["stats"]["calories"][1:]
    ):
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.calories.expended",
                "value": [{"fpVal": x["value"] - index["value"]}],
            }
        )
    """
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Calorie data successfully")


def UploadIfitDistanceToGoogle(IfitWorkoutJson):
    '''Function that uploads distance data from iFit workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[4]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.start
            + IfitWorkoutJson.lists["meters"][0]["offset"] * 1000000,
            "dataTypeName": "com.google.distance.delta",
            "value": [{"fpVal": IfitWorkoutJson.lists["meters"][0]["value"]}],
        }
    )
    for index, x in zip(
        IfitWorkoutJson.lists["meters"], IfitWorkoutJson.lists["meters"][1:]
    ):
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.distance.delta",
                "value": [{"fpVal": x["value"] - index["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Distance data successfully")

def UploadIfitGPSToGoogle(IfitWorkoutJson):
    '''Function that uploads distance data from iFit workout to Google Fit'''
    '''Create a List with Coordinates and Distances correlating'''
    WORKOUT_DETAILS_URL = "https://api.ifit.com/v1/workouts/" + IfitWorkoutJson.stats["workout_id"]
    WORKOUT_DETAILS = http.get(WORKOUT_DETAILS_URL, headers=IFIT_HIST_HEADERS).json()
    COORDINATES_WITH_DISTANCE = []
    sum = 0
    for coordinate, next_coordinate in zip(WORKOUT_DETAILS["geo"]["path"]["coordinates"], WORKOUT_DETAILS["geo"]["path"]["coordinates"][1:]):
        distance_between_GPS = haversine(next_coordinate, coordinate)
        next_coordinate.append(distance_between_GPS)
        sum = sum + next_coordinate[2]
        distance_ran = {}
        distance_ran["latitude"] = next_coordinate[1]
        distance_ran["longitude"] = next_coordinate[0]
        distance_ran["distance"] = sum
        COORDINATES_WITH_DISTANCE.append(distance_ran)

    '''Create a list with distances and timestamps'''

    DISTANCE_WITH_TIMESTAMP = []
    for x in IfitWorkoutJson.lists["meters"]:
        timestamp_distance = {}
        timestamp_distance["timestamp"] = IfitWorkoutJson.start + x["offset"]
        timestamp_distance["distance"] = x["value"]
        DISTANCE_WITH_TIMESTAMP.append(timestamp_distance)
    '''Create a list with elevations and timestamps'''

    ELEVATION_WITH_TIMESTAMP = []
    for x in IfitWorkoutJson.lists["elevation"]:
        timestamp_elevation = {}
        timestamp_elevation["timestamp"] = IfitWorkoutJson.start + x["offset"]
        timestamp_elevation["elevation"] = x["value"]
        ELEVATION_WITH_TIMESTAMP.append(timestamp_elevation)    

    '''Remove excess GPS points that were not actually arrived at'''
    actual_run_distance = DISTANCE_WITH_TIMESTAMP[-1]["distance"]
    ACTUAL_COORDINATES_WITH_DISTANCE = []
    for x in COORDINATES_WITH_DISTANCE:
        if x["distance"] < actual_run_distance:
            ACTUAL_COORDINATES_WITH_DISTANCE.append(x)
    COORDINATES_WITH_DISTANCE = ACTUAL_COORDINATES_WITH_DISTANCE
    ''' Create a list of distances only to get index of correct entry'''
    DISTANCE_LIST = []
    for x in DISTANCE_WITH_TIMESTAMP:
        DISTANCE_LIST.append(x["distance"])

    ''' Create a List of timestamps with Coordinates'''
    COORDINATES_WITH_TIMESTAMPS = []
    for x in COORDINATES_WITH_DISTANCE:
        closest_value = closest(DISTANCE_LIST, x["distance"])
        index_closest_value = DISTANCE_LIST.index(closest_value)
        item = {}
        item["latitude"] = x["latitude"]
        item["longitude"] = x["longitude"]
        item["timestamp"] = DISTANCE_WITH_TIMESTAMP[index_closest_value]["timestamp"]
        COORDINATES_WITH_TIMESTAMPS.append(item)
    ''' Create a list of timestamps in Elevation List to get indexes'''
    ELEVATION_LIST = []
    for x in ELEVATION_WITH_TIMESTAMP:
        ELEVATION_LIST.append(x["timestamp"])
    ''' APPEND ELEVATIONS TO COORDINATES WITH TIMESTAMPS'''
    if len(ELEVATION_LIST) != 0:
        for x in COORDINATES_WITH_TIMESTAMPS:
            closest_value = closest(ELEVATION_LIST, x["timestamp"])
            index_closest_value = ELEVATION_LIST.index(closest_value)
            x["elevation"] = ELEVATION_WITH_TIMESTAMP[index_closest_value]["elevation"]


    if not WORKOUT_DETAILS["has_geo_data"]:
        print("No Geo Data for workout")
    else:
        google_datapoint = {}
        google_datapoint.update(
            minStartTimeNs=IfitWorkoutJson.start,
            maxEndTimeNs=IfitWorkoutJson.end,
            dataSourceId=GOOGLE_DATA_SOURCES[7]["datasourceid"],
            point=[],
        )

        google_datapoint["point"].append(
            {
                "startTimeNanos": IfitWorkoutJson.start,
                "endTimeNanos": IfitWorkoutJson.start
                + IfitWorkoutJson.lists["meters"][0]["offset"] * 1000000,
                "dataTypeName": "com.google.location.sample",
                "value": [{"fpVal": WORKOUT_DETAILS["geo"]["path"]["coordinates"][0][1]},{"fpVal": WORKOUT_DETAILS["geo"]["path"]["coordinates"][0][0]}, {"fpVal": 5}, {"fpVal": 0}],
            }
        )
        if len(IfitWorkoutJson.lists["elevation"]) != 0:
            for x in COORDINATES_WITH_TIMESTAMPS:
                google_datapoint["point"].append(
                    {
                        "startTimeNanos": x["timestamp"],
                        "endTimeNanos": x["timestamp"] + 1,
                        "dataTypeName": "com.google.location.sample",
                        "value": [{"fpVal": x["latitude"]}, {"fpVal": x["longitude"]}, {"fpVal": 5}, {"fpVal": x["elevation"]}],
                    }
                )
            google_datapoint["point"].append(
                {
                    "startTimeNanos": IfitWorkoutJson.end - 1,
                    "endTimeNanos": IfitWorkoutJson.end,
                    "dataTypeName": "com.google.location.sample",
                    "value": [{"fpVal": COORDINATES_WITH_TIMESTAMPS[-1]["latitude"]},{"fpVal": COORDINATES_WITH_TIMESTAMPS[-1]["longitude"]}, {"fpVal": 5}, {"fpVal": COORDINATES_WITH_TIMESTAMPS[-1]["elevation"]}],
                }
            )
        else:
            for x in COORDINATES_WITH_TIMESTAMPS:
                google_datapoint["point"].append(
                    {
                        "startTimeNanos": x["timestamp"],
                        "endTimeNanos": x["timestamp"] + 1,
                        "dataTypeName": "com.google.location.sample",
                        "value": [{"fpVal": x["latitude"]}, {"fpVal": x["longitude"]}, {"fpVal": 5}],
                    }
                )
            google_datapoint["point"].append(
                {
                    "startTimeNanos": IfitWorkoutJson.end - 1,
                    "endTimeNanos": IfitWorkoutJson.end,
                    "dataTypeName": "com.google.location.sample",
                    "value": [{"fpVal": COORDINATES_WITH_TIMESTAMPS[-1]["latitude"]},{"fpVal": COORDINATES_WITH_TIMESTAMPS[-1]["longitude"]}, {"fpVal": 5}, {"fpVal": 0}],
                }
            )

        datasetId = (
            str(google_datapoint["minStartTimeNs"])
            + "-"
            + str(google_datapoint["maxEndTimeNs"])
        )

        try:
            service.users().dataSources().datasets().patch(
                userId="me",
                dataSourceId=google_datapoint["dataSourceId"],
                datasetId=datasetId,
                body=google_datapoint,
                ).execute()
        except HttpError as error:
            raise error
        print("Uploaded Workout GPS data successfully")


def UploadIfitStepsToGoogle(IfitWorkoutJson):
    '''Function that uploads Step data from iFit workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[5]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.end,
            "dataTypeName": "com.google.step_count.delta",
            "value": [{"intVal": IfitWorkoutJson.stats["summary"]["total_steps"]}],
        }
    )
    """
    for index, x in zip(
        IfitWorkoutJson["stats"]["steps"], IfitWorkoutJson["stats"]["steps"][1:]
    ):
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
                + x["offset"] * 1000000,
                "dataTypeName": "com.google.step_count.delta",
                "value": [{"intVal": (x["value"] - index["value"])}],
            }
        )
    """
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Steps data successfully")


def UploadIfitSessionToGoogle(IfitWorkoutJson):
    '''Function that creates a workout on Google Fit and gives it a name and the activity type'''
    if IfitWorkoutJson.type == "run":
        fit_activity_type = 8
    session_body = {}
    session_body.update(
        id=IfitWorkoutJson.id,
        name=IfitWorkoutJson.title,
        startTimeMillis=IfitWorkoutJson.stats["start"],
        endTimeMillis=IfitWorkoutJson.stats["end"],
        application={"name": "iFit-Sync"},
        activityType=fit_activity_type,
    )

    try:
        service.users().sessions().update(userId="me", sessionId=IfitWorkoutJson.id, body=session_body,).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Session data successfully")

def UploadIfitActivityToGoogle(IfitWorkoutJson):
    '''This function populates the Active Time for the Google Fit Workout created'''
    if IfitWorkoutJson.type == "run":
        fit_activity_type = 8
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end,
        dataSourceId=GOOGLE_DATA_SOURCES[6]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson.start,
            "endTimeNanos": IfitWorkoutJson.end,            
            "dataTypeName": "com.google.activity.segment",
            "value": [{"intVal": fit_activity_type}],
        }
    )
    
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Activity data successfully")
def UploadIfitInclineToGoogle(IfitWorkoutJson):
    '''Function to Upload Incline data from iFit to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end + 1,
        dataSourceId=GOOGLE_DATA_SOURCES[8]["datasourceid"],
        point=[],
    )


    for x in IfitWorkoutJson.lists["incline"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": IfitWorkoutJson.start + x["offset"] * 1000000,
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000 + 1,
                "dataTypeName": "com.ifitsync.treadmillincline.degrees",
                "value": [{"fpVal": x["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Incline data successfully")    

def UploadIfitElevationToGoogle(IfitWorkoutJson):
    '''Function to Upload Elevation data from iFit to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson.start,
        maxEndTimeNs=IfitWorkoutJson.end + 1,
        dataSourceId=GOOGLE_DATA_SOURCES[9]["datasourceid"],
        point=[],
    )


    for x in IfitWorkoutJson.lists["elevation"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": IfitWorkoutJson.start + x["offset"] * 1000000,
                "endTimeNanos": IfitWorkoutJson.start
                + x["offset"] * 1000000 + 1,
                "dataTypeName": "com.ifitsync.treadmill.elevation",
                "value": [{"fpVal": x["value"]}],
            }
        )
    datasetId = (
        str(google_datapoint["minStartTimeNs"])
        + "-"
        + str(google_datapoint["maxEndTimeNs"])
    )

    try:
        service.users().dataSources().datasets().patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
            ).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Elevation data successfully")   

""" Check if the Google Data Sources don't exist and create them"""
for x in GOOGLE_DATA_SOURCES:
    if not CheckGoogleDataSourceExists(x["datasourceid"]):
        y = x.pop("datasourceid")
        CreateGoogleDataSource(x)
'''Function to check when the last time the script was run and upload just the workouts that have been added since'''
if path.exists('last_run_time.json'):
    with open('last_run_time.json') as timestamp_file:
        timestampdict = json.load(timestamp_file)
    last_run_time = timestampdict["last_run_time"]
else:
    last_run_time = 0
for last_workout in HISTORY_JSON:
    y = HISTORY(last_workout)
    if y.start_time > last_run_time:
        UploadIfitCaloriesToGoogle(y)
        UploadIfitDistanceToGoogle(y)
        UploadIfitHrToGoogle(y)
        UploadIfitSpeedToGoogle(y)
        UploadIfitStepsToGoogle(y)
        UploadIfitWattsToGoogle(y)
        UploadIfitSessionToGoogle(y)
        UploadIfitActivityToGoogle(y)
        UploadIfitInclineToGoogle(y)
        UploadIfitElevationToGoogle(y)
        UploadIfitGPSToGoogle(y)
    else:
        print(y.title + " already uploaded")


'''This creates the timestamp that will show when the script ran last'''

secondssinceepoch = round(time.time() * 1000)
timestampjson = {}
timestampjson["last_run_time"] = secondssinceepoch
with open('last_run_time.json', 'w') as timestamp_file:
    json.dump(timestampjson, timestamp_file)

