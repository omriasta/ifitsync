from get_googleaccount import main
from get_ifitaccount import FEED_JSON, HISTORY_JSON
from google_datasources import GOOGLE_DATA_SOURCES
from googleapiclient.errors import HttpError
import json
import time


service = main()
'''Assign Workout Name and ID from feed to History'''
for x in HISTORY_JSON:
    workout_id = x["id"]
    workout_name = next(item for item in FEED_JSON if item["id"] == workout_id)["title"]
    workout_date = next(item for item in FEED_JSON if item["id"] == workout_id)["date"]
    x["name"] = workout_name
    x["date"] = workout_date


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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[0]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["start"] * 1000000
            + IfitWorkoutJson["stats"]["bpm"][0]["offset"],
            "dataTypeName": "com.google.heart_rate.bpm",
            "value": [{"fpVal": IfitWorkoutJson["stats"]["bpm"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson["stats"]["bpm"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[1]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["start"] * 1000000
            + IfitWorkoutJson["stats"]["mps"][0]["offset"],
            "dataTypeName": "com.google.speed",
            "value": [{"fpVal": IfitWorkoutJson["stats"]["mps"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson["stats"]["mps"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[2]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["start"] * 1000000
            + IfitWorkoutJson["stats"]["watts"][0]["offset"],
            "dataTypeName": "com.google.power.sample",
            "value": [{"fpVal": IfitWorkoutJson["stats"]["watts"][0]["value"]}],
        }
    )
    for x in IfitWorkoutJson["stats"]["watts"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[3]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["end"] * 1000000,
            "dataTypeName": "com.google.calories.expended",
            "value": [{"fpVal": IfitWorkoutJson["summary"]["total_calories"]}],
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[4]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["start"] * 1000000
            + IfitWorkoutJson["stats"]["meters"][0]["offset"],
            "dataTypeName": "com.google.distance.delta",
            "value": [{"fpVal": IfitWorkoutJson["stats"]["meters"][0]["value"]}],
        }
    )
    for index, x in zip(
        IfitWorkoutJson["stats"]["meters"], IfitWorkoutJson["stats"]["meters"][1:]
    ):
        google_datapoint["point"].append(
            {
                "startTimeNanos": google_datapoint["point"][
                    len(google_datapoint["point"]) - 1
                ]["endTimeNanos"],
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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


def UploadIfitStepsToGoogle(IfitWorkoutJson):
    '''Function that uploads Step data from iFit workout to Google Fit'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[5]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["end"] * 1000000,
            "dataTypeName": "com.google.step_count.delta",
            "value": [{"intVal": IfitWorkoutJson["summary"]["total_steps"]}],
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
    session_body = {}
    session_body.update(
        id=IfitWorkoutJson["id"],
        name=IfitWorkoutJson["name"],
        startTimeMillis=IfitWorkoutJson["start"],
        endTimeMillis=IfitWorkoutJson["end"],
        application={"name": "iFit-Sync"},
        activityType=58,
    )

    try:
        service.users().sessions().update(userId="me", sessionId=IfitWorkoutJson["id"], body=session_body,).execute()
    except HttpError as error:
        raise error
    print("Uploaded Workout Session data successfully")

def UploadIfitActivityToGoogle(IfitWorkoutJson):
    '''This function populates the Active Time for the Google Fit Workout created'''
    google_datapoint = {}
    google_datapoint.update(
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000,
        dataSourceId=GOOGLE_DATA_SOURCES[6]["datasourceid"],
        point=[],
    )

    google_datapoint["point"].append(
        {
            "startTimeNanos": IfitWorkoutJson["start"] * 1000000,
            "endTimeNanos": IfitWorkoutJson["end"] * 1000000,            
            "dataTypeName": "com.google.activity.segment",
            "value": [{"intVal": 58}],
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000 + 1,
        dataSourceId=GOOGLE_DATA_SOURCES[8]["datasourceid"],
        point=[],
    )


    for x in IfitWorkoutJson["stats"]["incline"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": IfitWorkoutJson["start"] * 1000000 + x["offset"] * 1000000,
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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
        minStartTimeNs=IfitWorkoutJson["start"] * 1000000,
        maxEndTimeNs=IfitWorkoutJson["end"] * 1000000 + 1,
        dataSourceId=GOOGLE_DATA_SOURCES[9]["datasourceid"],
        point=[],
    )


    for x in IfitWorkoutJson["stats"]["elevation"][1:]:
        google_datapoint["point"].append(
            {
                "startTimeNanos": IfitWorkoutJson["start"] * 1000000 + x["offset"] * 1000000,
                "endTimeNanos": IfitWorkoutJson["start"] * 1000000
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
with open('last_run_time.json') as timestamp_file:
    timestampdict = json.load(timestamp_file)
last_run_time = timestampdict["last_run_time"]
for last_workout in HISTORY_JSON:
    if last_workout["start"] > last_run_time:
        UploadIfitCaloriesToGoogle(last_workout)
        UploadIfitDistanceToGoogle(last_workout)
        UploadIfitHrToGoogle(last_workout)
        UploadIfitSpeedToGoogle(last_workout)
        UploadIfitStepsToGoogle(last_workout)
        UploadIfitWattsToGoogle(last_workout)
        UploadIfitSessionToGoogle(last_workout)
        UploadIfitActivityToGoogle(last_workout)
        UploadIfitInclineToGoogle(last_workout)
        UploadIfitElevationToGoogle(last_workout)
    else:
        print(last_workout["name"] + " already uploaded")


'''This creates the timestamp that will show when the script ran last'''
secondssinceepoch = round(time.time() * 1000)
timestampjson = {}
timestampjson["last_run_time"] = secondssinceepoch
with open('last_run_time.json', 'w') as timestamp_file:
    json.dump(timestampjson, timestamp_file)
