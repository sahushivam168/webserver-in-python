from http import cookies
from ServerServices import *
import json
import os
import uuid
from flask import make_response
from http.server import HTTPServer,BaseHTTPRequestHandler
class MyWebServer(BaseHTTPRequestHandler):
 cookieDS=dict() 
 def do_GET(self):
   self.send_response(200)   
   IP=self.client_address[0]
   response="<h1>error : 404</h1>"
   appPath=os.getcwd()+"\\applications"  
   applist=os.listdir(appPath) 
   i=0
   while i<len(applist):
        if self.path=="/":
           response="<h1>Wellcome to MyWebServer<h1>"
           break
        #----------------------------------------------------------------
        pri_path=os.getcwd()+"\\applications\\"+applist[i]+"\\private"
        pub_path=os.getcwd()+"\\applications\\"+applist[i]+"\\public"
        pri_List=os.listdir(pri_path)
        pub_List=os.listdir(pub_path)      
        if any("Deployment.json" in s for s in pri_List):
           deploy=open(pri_path+"\Deployment.json")
           jsonfile=json.load(deploy)
           HomePage=jsonfile["HomePage"]
           ContextName=jsonfile["ContextName"]
                           
           if ContextName!="":
              if self.path=="/"+ContextName:
                 if HomePage!="":
                    response=open(pub_path+"\\"+HomePage).read()
                 else:
                    if any("index.html" in s for s in pub_List): 
                       response=open(pub_path+"\index.html").read()
                    else:
                       response="<h1>error : 404</h1>"
           else: 
               response="<h1>error : 404</h1>"
        
     
                 
        #----------------------------------------------------------------
        if self.path=="/"+applist[i]:
           found=1                 
           if any("Deployment.json" in s for s in pri_List):
               deploy=open(pri_path+"\Deployment.json")
               jsonfile=json.load(deploy)
               HomePage=jsonfile["HomePage"]
               if HomePage=="":
                   found=0
               else:
                   found=0
           else:
               found=0
           if found==0:               
               if any("index.html" in s for s in pub_List): 
                  response=open(pub_path+"\index.html").read()
               else:
                  response="<h1>error : 500</h1>"
           break
        i=i+1
   #--------------------------------------------
   isCookie=self.headers.get('Cookie')
   if isCookie!=None: 
     print(isCookie)
     cookieAry=isCookie.split("=")
     name=cookieAry[0]
     value=cookieAry[1]
     print("Name :"+name)
     print("Value :"+value) 

   cook1=cookies.SimpleCookie();
   cook1["firstCookie"]=9442164781;
   cook1["firstCookie"]["max-age"]=30;
   self.send_response(200)
   self.send_header('content-type','text/html')
   self.send_header('Set-Cookie',cook1.output(header=''))             
   
   self.end_headers()
   self.wfile.write(bytes(response,"utf-8"))
try:
 confFile=open('conf\configuration.json')
 port=json.load(confFile)["port"]
 httpServer=HTTPServer(('',port),MyWebServer)
 print("------------------Server Started on port number ",port,"-----------------------")
 httpServer.serve_forever()
except FileNotFoundError:
 print("Configuration File Not Found")   
except KeyboardInterrupt:
 print('Shutting down server')
 httpServer.socket.close()