def process(Req,Res):
 print("Process Method run")
 file=Req.fileWrapper;
 print(file.getFileName())
 print(file.getFilePath())
 Res.setContentType("text/html")
 Res.print("File was Uploaded.")