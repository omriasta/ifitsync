# ifitsync
## iFit now has an android tv app. If anyone would like to try and get the client id and traffic for this app, we may be able to get an easier authentication flow for the script.

Currently iFit does not have any documentation on the API and there is no way to integrate an app using their website. For now, you will have to figure out how to get Client ID and Secret on your own. It is not too hard. I have an iFit treadmill so that is the only thing this is written for but if you look at the code you should be able to tweak it to work with other equipment or even other services beyond google fit.
The project files are separated so you can use just "get_ifitaccount.py" to get the JSON responses from the API and then write some other code to upload to other services.

INSTRUCTIONS:

Get client id and secret for ifit api, I can't give this out but if you do some digging it's possible to get this from the android application

Place these in the const.py.template file in the respective places and then rename the file const.py

Go to https://console.developers.google.com

Create a new project and give it a name

Under Library search for fitness api and click on it, then enable the api

Then go to credentials and create new credentials, download the file and save it as credentials.json in the folder
(This follows the instructions here: https://developers.google.com/docs/api/quickstart/python)

Create a virtual environment: python3 -m venv venv

Activate the Virtual environment: source venv/bin/activate

Install requirements: pip install -r requirements.txt

Run the script: python ifitsync.py

Enter ifit user and pass when prompted

A browser should open and prompt you to sign in to google and grant access to a some Google Fit related options, allow them all

Close the browser when prompted and wait for the script to continue

You should see the results of uploaded datasets for each aspect of each workout.

After you go through this once, you will not be prompted for credentials again as the script will now use refresh tokens for both google and ifit.

Currently supports uploading the following:
- Heart Rate which is sampled throughout the workout
- Speed sampled throughout the workout
- Power in watts sampled throughout the workout
- Calories expended, this is uploaded as a total for the entire workout
- Distance sampled throughout the workout
- Step count, this is uploaded as a total for the entire workout
- Workout name taken from iFit
- Elevation Data in Meters (as a custom datatype)
- Treadmill Incline Degrees (as a custom datatype)
- Location/Elevation GPS data is now uploaded for iFit workouts that are based on a Google Maps Route.

Some notes and suggestions regarding the script can be found on the Wiki:
https://github.com/omriasta/ifitsync/wiki
