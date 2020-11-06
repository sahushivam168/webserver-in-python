class Request():
 ds=dict()
 fileWrapper="";
 date="";
 reqPath="";
 def processRequest(self,request):
  lists=request.split("&")
  for field in lists:
   list=field.split("=")
   self.ds.update({list[0]:list[1]})
 def getAttributes(self,field):
  return self.ds[field]
 def getFileWrapper(self):
  return fileWrapper
 def setFileWrapper(self,fileWrapper):
  self.fileWrapper=fileWrapper
 def requestForward(self,path):
  self.reqPath=path;
 
class Response():
 list=[]
 contentType=""
 isPrint=False;
 def print(self,pString):
  self.isPrint=True;
  self.list.append(pString)
 def setContentType(self,contentTypeString):
  self.contentType=contentTypeString

class FileWrapper():
 fileDetails=dict()
 def setFileDetails(self,fileName,path):
   return  self.fileDetails.update({"filename":fileName,"path":path})
 def getFileName(self):
  return  self.fileDetails["filename"]
 def getFilePath(self):
  return self.fileDetails["path"]

class Date():
 data="";
 def getDate(self):
  return self.date
 def setDate(self,date):
  self.date=date;