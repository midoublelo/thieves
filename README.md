# thieves
Thieves is a concurrent, thread-safe Google Drive uploader library. Will be releasing version on pip soon, but for now just include local file.

## Usage
Thieves uses pydrive which requires credentials from a Cloud Platform project. You can create one by clicking 'Enable the Drive API' here: https://developers.google.com/drive/api/v3/quickstart/python. Then save the file 'credentials.json' and rename it to 'client_secrets.json'. Now you can start writing code!

First, create a Thief. A Thief is a concurrent, thread-safe uploader that will upload all files in a folder it is given.
```py
import thieves

folder = Thief(<path>)
```

Now that you have created a Thief, you have to authenticate with Google Drive.

```py
folder = Thief(<path>)
folder.auth()
```

The first time you authenticate it will open in a web browser and allow your Cloud Platform project to connect. Afterwards, Thieves will automatically save your credentials to a file and will refer to those instead.

```py
folder = Thief(<path>)
folder.auth()
folder.upload()
```

Now that you have authenticated you can upload the folder.
