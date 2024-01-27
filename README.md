# BITS Calendar Maker

Quickly add your timetable into Google Calendar

## Prerequisites

To run this quickstart, you need the following prerequisites:

- <a href="https://developers.google.com/workspace/guides/create-project" target="_blank" class="external">A Google Cloud project</a>
- A Google account with Google Calendar enabled.

## Create a Google Cloud Project

1. In the Google Cloud console, go to **Menu menu** > **IAM & Admin** > **Create a Project**.
   <a href="https://console.cloud.google.com/projectcreate" class="button button-primary" target="console">Go to Create a Project</a>
2. In the **Project Name** field, enter a any name for your project.
3. Click **Create**. The Google Cloud console navigates to the Dashboard page and your project is created within a few minutes.

## Setting up the enviroment

To complete this quickstart, set up your environment.

### Enable the API

Before using Google APIs, you need to turn them on in a Google Cloud project. You can turn on one or more APIs in a single Google Cloud project.

- In the Google Cloud console, enable the Google Calendar API.
  <a href="https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com" class="button button-primary" target="console">Enable the API</a>

### Configure the OAuth consent screen

1. In the Google Cloud console, go to **Menu menu** > **APIs & Services** > **OAuth consent screen**.
   <a href="https://console.cloud.google.com/apis/credentials/consent" class="button button-primary" target="console">Go to OAuth consent screen</a>
2. Select the **External** for user type for your app, then click **Create**.
3. Complete the app registration form (only items marked with \*) , then click **Save and Continue**.
4. Click **Save and Continue** again.
5. Under **Test users**, click **Add users**.
6. Enter your email address, then click **Save and Continue**.
7. Review your app registration summary. To make changes, click **Edit**. If the app registration looks OK, click **Back to Dashboard**.

### Authorize credentials for a desktop application

1. In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
   <a href="https://console.cloud.google.com/apis/credentials" class="button button-primary" target="console">Go to Credentials</a>

2. Click **Create Credentials** > **OAuth client ID**.
3. Click **Application type** > **Desktop app**.
4. In the **Name** field, type a name for the credential. This name is only shown in the Google Cloud console.
5. Click **Create**. The OAuth client created screen appears, showing your new Client ID and Client secret.
6. Click **OK**. The newly created credential appears under OAuth 2.0 Client IDs.
7. Save the downloaded JSON file as **credentials.json**, and move the file to your working directory.

### Running the Program (Windows)

- Download the exe file
  <a href="https://github.com/kevin-samson/BITS-Calendar-Maker/releases/download/v0.0.2/main.exe" class="button button-primary" target="console">Download exe file</a>
- Make sure **credentials.json** and **main.exe** are in the same folder
- Run main.exe
  **Note:** If you get Somthing is wrong error, please copy the link and paste it in an incognito tab and login with your email
