from get_googleaccount import main
from get_ifitaccount import FEED_JSON, HISTORY_JSON
from google_datasources import GOOGLE_DATA_SOURCES
from googleapiclient.errors import HttpError
import json


service = main()
for x in HISTORY_JSON:
    workout_id = x["id"]
    workout_name = next(item for item in FEED_JSON if item["id"] == workout_id)["title"]
    workout_date = next(item for item in FEED_JSON if item["id"] == workout_id)["date"]
    x["name"] = workout_name
    x["date"] = workout_date


def CheckGoogleDataSourceExists(dataSourceId):
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
    try:
        service.users().dataSources().create(
            userId="me", body=GoogleDataSourceJson
        ).execute()
    except HttpError as error:
        if "40" in str(error):
            raise error

    print("Datasource successfully created")


def UploadIfitHrToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitSpeedToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitWattsToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitCaloriesToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitDistanceToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitStepsToGoogle(IfitWorkoutJson):
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

    test = (
        service.users()
        .dataSources()
        .datasets()
        .patch(
            userId="me",
            dataSourceId=google_datapoint["dataSourceId"],
            datasetId=datasetId,
            body=google_datapoint,
        )
        .execute()
    )
    print(test)


def UploadIfitSessionToGoogle(IfitWorkoutJson):
    session_body = {}
    session_body.update(
        id=IfitWorkoutJson["id"],
        name=IfitWorkoutJson["name"],
        startTimeMillis=IfitWorkoutJson["start"],
        endTimeMillis=IfitWorkoutJson["end"],
        application={"name": "iFit-Sync"},
        activityType=88,
    )

    test = (
        service.users()
        .sessions()
        .update(userId="me", sessionId=IfitWorkoutJson["id"], body=session_body,)
        .execute()
    )
    print(test)


""" Check if the Google Data Sources don't exist and create them"""
for x in GOOGLE_DATA_SOURCES:
    if not CheckGoogleDataSourceExists(x["datasourceid"]):
        y = x.pop("datasourceid")
        CreateGoogleDataSource(x)

for last_workout in HISTORY_JSON:
    UploadIfitCaloriesToGoogle(last_workout)
    UploadIfitDistanceToGoogle(last_workout)
    UploadIfitHrToGoogle(last_workout)
    UploadIfitSpeedToGoogle(last_workout)
    UploadIfitStepsToGoogle(last_workout)
    UploadIfitWattsToGoogle(last_workout)
    UploadIfitSessionToGoogle(last_workout)
