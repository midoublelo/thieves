import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Thief:
    '''
    Creates a Thief at the given path.
    '''
    def __init__(self, path):
        self.path = path
        self.__curLoc__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def auth(self):
        '''
        Authenticates with Google Drive.
        '''
        self.gauth = GoogleAuth()
        if os.path.exists(os.path.join(self.__curLoc__, "client_secrets.json")):
            if os.path.exists(os.path.join(self.__curLoc__, "creds.txt")):
                self.gauth.LoadCredentialsFile("creds.txt")
                self.drive = GoogleDrive(self.gauth)
                self.http = self.drive.auth.Get_Http_Object()
            else:
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()
                gauth.SaveCredentialsFile("creds.txt")
        else:
            print("Error: 'client_secrets.json' missing.")

    def upload(self):
        '''
        Uploads contents of folder to Google Drive.
        '''
        if os.path.exists(os.path.join(self.__curLoc__, "pathlist.json")):
            with open('pathlist.json', 'r+') as pathFile:
                pathData = json.load(pathFile)
                if self.path in pathData:
                    self.folderId = pathData[self.path]
                else:
                    targetName = os.path.basename(os.path.normpath(self.path))
                    uploadFolder = self.drive.CreateFile({'title': targetName, "mimeType": "application/vnd.google-apps.folder"})
                    uploadFolder.Upload(param={"http": self.http})
                    addedFolder = { f"{self.path}": f"{uploadFolder['id']}" }
                    self.folderId = uploadFolder['id']
                    pathData.update(addedFolder)
                    pathFile.seek(0)
                    json.dump(pathData, pathFile)
            for filename in os.listdir(self.path):
                upload = self.drive.CreateFile({'title': filename,'parents': [{'id': self.folderId}]})
                upload.SetContentFile(self.path + "/" + filename)
                upload.Upload(param={"http": self.http})
            print(f"Uploaded: {self.path}")
        else:
            print("Error: 'pathlist.json' missing.")
            print("Creating 'pathlist.json'...")
            targetName = os.path.basename(os.path.normpath(self.path))
            uploadFolder = self.drive.CreateFile({'title': targetName, "mimeType": "application/vnd.google-apps.folder"})
            uploadFolder.Upload(param={"http": self.http})
            addedFolder = { f"{self.path}": f"{uploadFolder['id']}" }
            with open('pathlist.json', 'w') as pathFile:
                json.dump(addedFolder, pathFile)
            print("'pathlist.json' created. Please run again.")

folder = Thief("C:/Users/Millo/Desktop/Exedys/Projects/Thieves/thieves/test")
folder.auth()
folder.upload()