from base64 import encode
import requests
import json
import os
from time import sleep
from anaplanConnector.auth import Auth
from anaplanConnector.endpoints import Endpoints
from anaplanConnector.file import File

from pprint import pprint

class Connection:
    def __init__(self,email,password,workspaceId=None,modelId=None):
        self.email = email
        self.password = password
        self.workspaceId = workspaceId
        self.modelId = modelId
        self.token = None
        self.endpoints = Endpoints(workspaceId=workspaceId,modelId=modelId)
        self.file = File()

    def getToken(self):
        auth = Auth()
        self.token = auth.basicAuth(email=self.email,password=self.password,tokenEndpoint=self.endpoints.token)['tokenValue']
        self.authHeader = {'Authorization': f'AnaplanAuthToken {self.token}'}

    def makeRequest(self,method,url,headers={},**kwargs):
        if self.token == None:
            self.getToken()
        headers = {**self.authHeader, **headers}
        res = requests.request(method,url,headers=headers,**kwargs)
        return res.text

    def getWorkspaces(self,tenantDetails=False):
        return self.makeRequest('GET',f"{self.endpoints.workspaces}?tenantDetails={tenantDetails}", headers={'Accept' : 'application/json'})
    
    def getModels(self):
        return self.makeRequest('GET',self.endpoints.models(),headers={'Accept' : 'application/json'})
    
    def getFiles(self):
        return self.makeRequest('GET', self.endpoints.files(),headers={'Accept' : 'application/json'})

    def getFileIdByFilename(self,filename):
        res = json.loads(self.getFiles())
        fileId = list(filter(lambda x:x['name'] == filename, res['files']))[0]['id']
        print(f'fileId: {fileId}')
        return fileId

    def getProcesses(self):
        return self.makeRequest('GET', self.endpoints.processes(), headers={'Accept' : 'application/json'})
    
    def getProcessIdByName(self,processName):
        res = json.loads(self.getProcesses())
        processId = list(filter(lambda x:x['name']==processName,res['processes']))[0]['id']
        print(f'processId: {processId}')
        return processId

    def runProcess(self,processId):
        print(f'Running process: {processId}...')
        return self.makeRequest('POST', self.endpoints.runProcess(processId=processId), headers={'Content-Type' : 'application/json'}, data='{"localeName": "en_US"}')
    
    def loadFile(self,filepath,fileId):
        self.file.setFilepath(filepath)
        self.endpoints.fileId = fileId
        print(f'Uploading file {filepath} to Anaplan...')
        if self.file.chunkCount == 1:
            return self.makeRequest('PUT', self.endpoints.file(), headers={'Content-Type' : 'application/octet-stream'}, data=self.file.getFileData())
        else:
            # 1) Post chunk count
            data = { "chunkCount":self.file.chunkCount }
            self.makeRequest('POST', self.endpoints.file(), headers={'Content-Type' : 'application/octet-stream'}, data=json.dumps(data))
            # 2) PUT each chunk
            print(f'Total Number of chunks: {self.file.chunkCount}')
            chunkNum = 0
            for chunk in self.file.fileChunks():
                print(f'Loading chunk: {chunkNum+1}')
                self.makeRequest('PUT', self.endpoints.chunk(fileId,chunkNum), headers={'Content-Type' : 'application/octet-stream'}, data=chunk)
                chunkNum += 1

    def getExports(self):
        return self.makeRequest('GET', self.endpoints.exports(), headers={'Accept' : 'application/json'})

    def getExportIdByName(self,exportName):
        res = json.loads(self.getExports())
        exportId = list(filter(lambda x:x['name']==exportName, res['exports']))[0]['id']
        print(f'exportId: {exportId}')
        return exportId

    def export(self, exportId, filepath, encoding='utf-8'):
        res = json.loads(self.makeRequest('POST', self.endpoints.startExport(exportId), headers={'Content-Type' : 'application/json'}, data='{"localeName": "en_US"}'))
        taskId = res['task']['taskId']
        while True:
            sleep(2)
            res = json.loads(self.makeRequest('GET', self.endpoints.taskStatus(exportId,taskId), headers={'Accept' : 'application/json'}))
            taskState = res['task']['taskState']
            if taskState == 'COMPLETE':
                successful = res['task']['result']['successful']
                break
        if successful == True:
            res = json.loads(self.makeRequest('GET', self.endpoints.getNumChunks(exportId), headers={'Content-Type' : 'application/json'}))
            chunks = list(map(lambda x:x['id'],res['chunks']))
            # return chunks
            with open(filepath, "w", newline='', encoding=encoding) as file:
                for chunk in chunks:
                    print(f'Downloading chunk: {str(int(chunk)+1)}')
                    r = self.makeRequest('GET', self.endpoints.chunk(exportId,chunk), headers={'Content-Type' : 'application/json'})
                    file.write(r)
            return 'Success'
        else: raise Exception('Export failed')


            
