def process(Req,Res):
 #name=Req.getAttributes("name")
 #age=Req.getAttributes("age")
 #print(name)
 #print(age)
 Res.setContentType("text/html")
 Res.print("shivam")
 Res.print("<br>")
 Res.print("age")
 Res.print("21")
 Res.print("Saved.")