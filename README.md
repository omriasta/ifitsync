# ifitsync
Get client id and secret for ifit api, I can't give this out but if you do some digging it's possible to get this from the android application
Place these in the const.py.template file in the respective places and then rename the file const.py
go to https://console.developers.google.com
Create a new project and give it a name
Under Library search for fitness api and click on it, then enable the api
THen go to credentials and create new credentials, download the file and save it as credentials.json in the folder
(This follows the instructions here: https://developers.google.com/docs/api/quickstart/python)
create a virtual environment: python3 -m venv venv
Activate the Virtual environment: source venv/bin/activate
Install requirements: pip install -r requirements.txt
run the scripts: python ifitsync.py
Enter ifit user and pass when prompted
A browser should open and prompt you to sign in to google and grant access to a some Google Fit related options, allow them all
Close the browser when prompted and wait for the script to continue
You should see all the data that is being uploaded to google fit, I left this on for anyone troubleshooting until some error catching will be written
After you go through this once, you will not be prompted for credentials again as the script will now use refresh tokens for both google and ifit.
