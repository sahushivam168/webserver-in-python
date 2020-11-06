from ServerServices import *
import json
import  os
import uuid
import sys
import cgi
from datetime import datetime as dt
import time
from http import cookies
import cgitb; cgitb.enable()
from flask import Flask,request,url_for,render_template,make_response,redirect
from http.server import HTTPServer,BaseHTTPRequestHandler
class DataLoad():
  appData=dict()
  applist="" 
  def __init__(self):
   path=os.getcwd()+"\\applications"  
   self.applist=os.listdir(path)
   for appName in self.applist:
     DeployPath=os.getcwd()+"\\applications\\"+appName+"\\private\\Deployment.json"	
     if(os.path.exists(DeployPath)):
       Deploy=open(DeployPath)
       self.appData.update({appName:json.load(Deploy)})
     else:
       self.appData.update({appName:{}})

class WebServer(BaseHTTPRequestHandler):
 dataStructure=DataLoad()
 cookieDS=dict()
 stored_time=[] 

#----------------------------------some function related to py,psp
 def pspToPy(self):
   print("conversion psp to py");
 def runPyFile(self,fileName,appName):
   privateFilePath=os.getcwd()+"\\applications\\"+appName+"\\private" 
   publicFilePath=os.getcwd()+"\\applications\\"+appName+"\\public"              
   if os.path.isfile(privateFilePath+"\\"+fileName) or os.path.isfile(publicFilePath+"\\"+fileName):
    moduleName=""; 
    module="";
    


#----------------------------------------------Do_post start-------------
 def do_POST(self):
  print("Post method Invoke")
  response="error:404"
  contentType="text/html"
  Req=Request()
  Res=Response()
  appList=self.dataStructure.applist
  appData=self.dataStructure.appData.copy()
  upTime1=time.time()
  form=cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST'})
  fileName=form['filename'].filename
  new_fileName="";
  if fileName!='':
   contextName=""
   urlPattern=""
   queryStr=""
   url=self.path
   list=url.split("/",2)     
   contextName=list[1]
   subStr=""
   if url.find("?")!=-1:
     subStr=list[2]
     list=subStr.split("?",1)
     urlPattern=list[0]
     queryStr=list[1]
   else:
     if url.find("/",1)!=-1:
       subStr=list[2]
       list=subStr.split("/",1)
       urlPattern=list[0]
   contextFound="false"
   appName=""
   Res.list=[];
   if queryStr!="":
    Req.processRequest(queryStr)
   for appNames in appList: 
     data=appData.get(appNames)
     if data.get("ContextName")!="none" and data.get("ContextName")==contextName:
       contextFound="true"
       appName=appNames
       break
   if contextFound=="true":
     if urlPattern!="" and queryStr=="":         
          urlMapping=(appData.get(appName)).get("Url-Mapping")          
          if urlMapping!="none":
           x=0 
           while x<len(urlMapping):
             if urlMapping[x].get("url")==urlPattern:
               break 
             x=x+1                
           
           res=urlMapping[x].get("resource")
           defaultSize=200*1024*1024
           if len(res)>2: defaultSize=res[2]
           file_size=int(self.headers['Content-Length'])
           if int(defaultSize)>=file_size:
            upfilecontent=form['filename'].value  
            new_fileName=str(uuid.uuid1()) 
            fout=open(os.getcwd()+"\\uploadedFiles\\"+new_fileName+"."+fileName.split(".")[1],'wb')
            fout.write(upfilecontent)
            fout.close();
            print("File Saved.")
            upTime2=time.time()
            print(upTime2-upTime1)
            filewrapper=FileWrapper();
            filewrapper.setFileDetails(fileName,os.getcwd()+"\\uploadedFiles");
            Req.fileWrapper=filewrapper; 
            if res[1]=="Post":
             pyFile=os.getcwd()+"\\applications\\"+appName+"\\private" 
             sys.path.append(pyFile) 
             moduleName=res[0].strip(".py")
             module=__import__(moduleName)
             module.process(Req,Res)
             os.remove(os.getcwd()+"\\UploadedFiles\\"+new_fileName+"."+fileName.split(".")[1]);   
             contentType=Res.contentType
            else: 
             response="error : METHOD_NOT_ALLOWED"; 
           else:
             response="error : File Size is not accepted";  
  else:
     response="404 : File doesn't choose for Upload"
  self.send_response(200)
  self.send_header('content-type',contentType)
  self.end_headers()
  if len(Res.list)!=0:
    for clientRes in Res.list:
      self.wfile.write(bytes(clientRes,"utf-8"))
    Res.list=[];
  else:
    self.wfile.write(bytes(response,"utf-8"))
   
#----------------------------------------------Do_Get Start----------
 def do_GET(self):
   if self.path=="/favicon.ico":
    return;
   print("Get method Invoke")
   self.send_response(200)
   response="error : 404"
   cookie="";
   appList=self.dataStructure.applist
   appData=self.dataStructure.appData.copy()
   contextName=""
   urlPattern=""
   queryStr=""
   url=self.path
   list=url.split("/",2)     
   contextName=list[1]
   subStr=""
   if url.find("?")!=-1:
     subStr=list[2]
     list=subStr.split("?",1)
     urlPattern=list[0]
     queryStr=list[1]
   else:
     if url.find("/",1)!=-1:
       subStr=list[2]
       list=subStr.split("/",1)
       urlPattern=list[0]
   contextFound="false"
   appName=""
   contentType="text/html"
   Req=Request()
   if queryStr!="":
    Req.processRequest(queryStr)
   Res=Response()
   data="";  
   for appNames in appList: 
     data=appData.get(appNames)
     if data.get("ContextName")!="none" and data.get("ContextName")==contextName:
       contextFound="true"
       appName=appNames
       break
   
   if contextFound=="true":       
     if urlPattern=="" and queryStr=="":
        homepage=(appData.get(appName)).get("HomePage")
        Res.list=[];
        if homepage!="none":
          response=open(os.getcwd()+"\\applications\\"+appName+"\\public\\"+homepage).read()
        else:
          response="error:404"
     else:
        if urlPattern.find(".html")!=-1 and queryStr=="": 
          Res.list=[]; 
          response=open(os.getcwd()+"\\applications\\"+appName+"\\public\\"+urlPattern).read()
        else:          
           reqCookie=self.headers.get("Cookie") #------cookie setting-----
           name,value="","";
           uniqueID=0;                     
           if reqCookie!=None:                                    
              cookieAry=reqCookie.split("=")  
              name,value=cookieAry[0],cookieAry[1]
           if len(self.stored_time)!=0:
             if (time.time()/60)>self.stored_time[0]:               
               self.cookieDS.clear();               
               self.stored_time.pop(0)     
           if name=="bandu" and self.cookieDS.get("value")==value:              
              print(self.cookieDS.get("value")==value)              
              date=self.cookieDS.get("object")              
              Req.date=date;               
           else:
              self.stored_time.append((time.time()/60)+2);              
              date=Date();
              uniqueID=str(uuid.uuid1()) 
              self.cookieDS.update({"object":date,"value":uniqueID})  
              Req.date=date;
              cookie=cookies.SimpleCookie()
              cookie["bandu"]=uniqueID;              
              self.send_header('Set-Cookie',cookie.output(header=''))                           
           Res.list=[];     
           urlMapping=(appData.get(appName)).get("Url-Mapping")           
           if urlMapping!="none":
            x=0 
            while x<len(urlMapping):
             if urlMapping[x].get("url")==urlPattern:
               break 
             x=x+1
            print(urlMapping[x])                
            res=urlMapping[x].get("resource")
            if res[1]=="Get":           
             privateFilePath=os.getcwd()+"\\applications\\"+appName+"\\private" 
             publicFilePath=os.getcwd()+"\\applications\\"+appName+"\\public"              
             if os.path.isfile(privateFilePath+"\\"+res[0]) or os.path.isfile(publicFilePath+"\\"+res[0]):
              moduleName=""; 
              module="";              
              if (res[0].find(".py"))!=-1 :  
                fileName=res[0];              
                sys.path.append(privateFilePath)
                moduleName=fileName.strip(".py")              
                module=__import__(moduleName)
                os.chdir(privateFilePath);
                module.process(Req,Res)
                os.chdir("C:\\server_python");
                if Res.isPrint==False and Req.reqPath!="":                 
                   print((Req.reqPath).find(".py"));
                    
                   if os.path.exists(os.getcwd()+"\\applications\\"+appName+"\\public\\"+Req.reqPath)==True:
                      response="file exists";
                   else:
                      response="404"+"\n"+Req.reqPath+" - File doesn't exsits"               
                if Res.contentType!="": contentType=Res.contentType
                
              if (res[0].find(".psp"))!=-1 :                 
               if os.path.exists(os.getcwd()+"\\Store")==False:
                 os.mkdir(os.getcwd()+"\\Store")
               if os.path.exists(os.getcwd()+"\\Store\\"+res[0].strip(".psp")+"$psp.py")==False:            
                 pspfile=open(os.getcwd()+"\\applications\\"+appName+"\\public\\"+res[0],"r")
                 pspfilecontent=pspfile.readlines();
                 pspfile.close();
                 pyfile=open(os.getcwd()+"\\Store\\"+res[0].strip(".psp")+"$psp.py","w")
                 pyfile.write("def process(Req,Res):\n");
                 x=0;
                 while x<len(pspfilecontent):
                  if pspfilecontent[x].find("<%")!=-1:
                    x=x+1     
                    while pspfilecontent[x].find("%>")==-1:
                      pyfile.write(" "+pspfilecontent[x]);
                      x=x+1     
                  else: 
                    pspfilecontentline=pspfilecontent[x]
                    pspfilecontentline=pspfilecontentline.replace("\"","\\\"");    
                    pyfile.write(" Res.print(\""+pspfilecontentline.rstrip("\n")+"\")"+"\n");
                  x=x+1
                 pyfile.close();
               else:                 
                 mod_time_py=os.path.getctime(os.getcwd()+"\\Store\\"+res[0].strip(".psp")+"$psp.py");
                 mod_time_psp=os.path.getctime(os.getcwd()+"\\applications\\"+appName+"\\public\\"+res[0]);
                 print(str(mod_time_psp)+"|"+str(mod_time_py))  
                 if mod_time_py>mod_time_psp:                   
                   pspfile=open(os.getcwd()+"\\applications\\"+appName+"\\public\\"+res[0],"r")
                   pspfilecontent=pspfile.readlines();
                   pspfile.close();
                   pyfile=open(os.getcwd()+"\\Store\\"+res[0].strip(".psp")+"$psp.py","w")
                   pyfile.write("def process(Req,Res):\n");
                   x=0;
                   while x<len(pspfilecontent):
                    if pspfilecontent[x].find("<%")!=-1:
                     x=x+1     
                     while pspfilecontent[x].find("%>")==-1:
                      pyfile.write(" "+pspfilecontent[x]);
                      x=x+1     
                    else: 
                     pspfilecontentline=pspfilecontent[x]
                     pspfilecontentline=pspfilecontentline.replace("\"","\\\"");    
                     pyfile.write(" Res.print(\""+pspfilecontentline.rstrip("\n")+"\")"+"\n");
                    x=x+1
                   pyfile.close();
               sys.path.append(os.getcwd()+"\\Store")
               moduleName=res[0].strip(".psp")             
               module=__import__(moduleName+"$psp")
               os.chdir(publicFilePath);
               module.process(Req,Res)
               os.chdir("C:\\server_python");                                                                                
             else:
              response="404";
            else: 
             response="METHOD_NOT_ALLOWED"; 
   else:
     response="500"    
   
   self.send_header('content-type',contentType)  
   self.end_headers()
   print("isPrint : "+str(Res.isPrint))
   if len(Res.list)!=0 and Res.isPrint==True:     
     for clientRes in Res.list:
      self.wfile.write(bytes(clientRes,"utf-8"))
     Res.list=[];      
   else:
    self.wfile.write(bytes(response,"utf-8"))


confFile=open('conf\configuration.json')
port=json.load(confFile)["port"]
httpServer=HTTPServer(('',port),WebServer)
print("------------------Server Started on port number ",port,"-----------------------")
httpServer.serve_forever()