from sympy import *
u1re=Symbol("x1",real=True)
u1im=Symbol("x2",real=True)
u2re=Symbol("x3",real=True)
u2im=Symbol("x4",real=True)
u3re=Symbol("x5",real=True)
u3im=Symbol("x6",real=True)
u4re=Symbol("x7",real=True)
u4im=Symbol("x8",real=True)
ibfrre=Symbol("x9",real=True)
ibfrim=Symbol("x10",real=True)
ibtore=Symbol("x11",real=True)
ibtoim=Symbol("x12",real=True)
t=Symbol("x13",real=True)
f1=u1re-u2re-(1-0.00625*t)*(u3re-u4re)
f2=u1im-u2im-(1-0.00625*t)*(u3im-u4im)
f3=ibtore-(1-0.00625*t)*ibfrre
f4=ibtoim-(1-0.00625*t)*ibfrim
f=Matrix([f1,f2,f3,f4])
var=Matrix([u1re,u1im,u2re,u2im,u3re,u3im,u4re,u4im,ibfrre,ibfrim,ibtore,ibtoim,t])
J=f.jacobian(var)
#print pretty(J)
print hessian(f1,var)
 
ufrre = Symbol("x1",real=True)
ufrim = Symbol("x2",real=True)
utore = Symbol("x3",real=True)
utoim = Symbol("x4",real=True)
ibre = Symbol("x5",real=True)
ibim = Symbol("x6",real=True)
psp=Symbol("u1",real=True)
qsp=Symbol("u2",real=True)
ubre=ufrre-utore
ubim=ufrim-utoim
f1=re((ubre+I*ubim)*(ibre-I*ibim))-psp
f2=im((ubre+I*ubim)*(ibre-I*ibim))-qsp
xval=[ufrre,ufrim,utore,utoim,ibre,ibim]
h=hessian(f1,xval)
print pretty(h)
f=Matrix([f1,f2])
var=Matrix([ufrre,ufrim,utore,utoim,ibre,ibim])
J=f.jacobian(var)
print J
#initialization current source
f1=ibre
f2=ibim
f=Matrix([f1,f2])
var=Matrix([ufrre,ufrim,utore,utoim,ibre,ibim])
J=f.jacobian(var)
print J
#print pretty(hessian(re((ubre+I*ubim)*(ibre-I*ibim))-psp, [ufrre,ufrim,utore,utoim,ibre,ibim]))
print pretty(hessian(im((ubre+I*ubim)*(ibre-I*ibim))-psp, [ufrre,ufrim,utore,utoim,ibre,ibim]))
#f = x**2*y**3
#assert hessian(f, syms) == Matrix([[2*y**3, 6*x*y**2],[6*x*y**2, 6*x**2*y]])
