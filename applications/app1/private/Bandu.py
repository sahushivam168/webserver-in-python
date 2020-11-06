import datetime
def process(Req,Res):
 print("Process Method run for Bandu")
 date=Req.date
 newdt=datetime.date.today()
 date.setDate(newdt);
 Res.setContentType("text/html")
 Res.print(str(date.getDate()))