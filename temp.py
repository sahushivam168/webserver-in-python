import os
reqPath="reqPage.html";
app1="app1"
path=os.path.exists(os.getcwd()+"\\applications\\"+app1+"\\public\\"+reqPath)
print(os.getcwd()+"\\applications\\"+app1+"\\public\\"+reqPath);
print(path)