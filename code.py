testCases=int(input())
a=1;
while a<=testCases:
 p=int(input())
 q=int(input())
 pxy=[p][2];  
 pc=[p];
 xy=[q+1][q+1];
 b=0;
 while b<p:
   pxy[b][0]=int(input())
   pxy[b][1]=int(input())
   pc[b]=input()
   b=b+1;
 max=0;
 maxx;
 maxy;
 c=0;
 while c<=q:
   d=0;
   while d<=q:
     xy[c][d]=0;
     e=0;
     while e<p:
      x=pxy[e][0];
      y=pxy[e][1];
      direction=pc[e];
      if direction=='N':
        if d>y :
            xy[c][d]=xy[c][d]+1
      if direction=='S':
        if d<y :
             xy[c][d]=xy[c][d]+1
      if direction=='E':
         if c>x :
              xy[c][d]=xy[c][d]+1
      if direction=='W':
         if c<x:
              xy[c][d]=xy[c][d]+1
      if xy[c][d]>max:
          max=xy[c][d]
          maxx=c;
          maxy=d;
      e=e+1 
     d=d+1 
   print("Case #"+a+" : "+maxx+" "+maxy);
   c=c+1
 a=a+1;