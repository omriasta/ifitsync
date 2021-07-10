# ifitsync
## ClientId and Secret are now gathered by the script using web scraping If you already used the script previously you will have to reinstall requirements.txt and delete ifit-credentials.json.

Currently iFit does not have any documentation on the API and there is no way to integrate an app using their website. I have an iFit treadmill so that is the only thing this is written for but if you look at the code you should be able to tweak it to work with other equipment or even other services beyond google fit.
The project files are separated so you can use just "get_ifitaccount.py" to get the JSON responses from the API and then write some other code to upload to other services.

Windows users can use the exe file under dist, you will need to create the credentials.json file (listed below) and save it to the same directory as the exe. No need to worry about the virtual environment.

INSTRUCTIONS:

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

A browser should open and prompt you to sign in to google and grant access to some Google Fit related options, allow them all

Close the browser when prompted and wait for the script to continue

You should see the results of uploaded datasets for each aspect of each workout.

After you go through this once, you will not be prompted for credentials again as the script will now use refresh tokens for both google and ifit.

Currently supports uploading the following:
- Heart Rate which is sampled throughout the workout
- Speed sampled throughout the workout
- Power in watts sampled throughout the workout
- Calories expended sampled throughout workout
- Distance sampled throughout the workout
- Step count sampled throughout workout
- Workout name taken from iFit
- Elevation Data in Meters (as a custom datatype)
- Treadmill Incline Degrees (as a custom datatype)
- Location/Elevation GPS data is now uploaded for iFit workouts that are based on a Google Maps Route

Some notes and suggestions regarding the script can be found on the Wiki:
https://github.com/omriasta/ifitsync/wiki
Below are screenshots of a workout from iFit and how it appears in Google Fit:
<table>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/11823048/123702727-7bfb5c80-d831-11eb-8f5d-091b942faa85.png"></td>
    <td valign="top"><img src="https://user-images.githubusercontent.com/11823048/123702717-79990280-d831-11eb-9e99-053850f50ae6.png"></td>
  </tr>
 </table>
