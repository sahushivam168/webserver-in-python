#include<stdio.h>
int main()
{
int testCases;
scanf("%d",&testCases);
int a;
for(a=1;a<=testCases;++a)
{
int p,q;
scanf("%d %d",&p,&q);
//printf("%d %d",p,q);
int pxy[p][2];
char pc[p];
int xy[q+1][q+1];
for(int b=0;b<p;++b)
{
scanf("%d %d %c",&pxy[b][0],&pxy[b][1],&pc[b]);
}
int max=0,maxx,maxy;
for(int c=0;c<=q;++c)
{
for(int d=0;d<=q;++d)
{
xy[c][d]=0;
for(int e=0;e<p;++e)
{
int x=pxy[e][0];
int y=pxy[e][1];
int direction=pc[e];
//north-positive y,south-negative y,east-positive x,west-negative x
if(direction=='N')
{
if(d>y) ++xy[c][d]; 
}
if(direction=='S')
{
if(d<y) ++xy[c][d]; 
}
if(direction=='E')
{
if(c>x) ++xy[c][d];
}
if(direction=='W')
{
if(c<x) ++xy[c][d];
}
}
if(xy[c][d]>max)
{
max=xy[c][d],
maxx=c;
maxy=d;
}
}
}
printf("Case #%d: %d %d\n",a,maxx,maxy);
}
return 0;
}
