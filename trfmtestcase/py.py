import numpy as np
zseqs=np.array([[0.1414+1j*0.5353,0.0361+1j*0.3225,0.0361+1j*0.2752],[0.0361+1j*0.3225,0.1414+1j*0.5353,0.0361+1j*0.2955],[0.0361+1j*0.2752,0.0361+1j*0.2955,0.1414+1j*0.5353]])
zseql=np.array([[0.1907+1j*0.5035,0.0607+1j*0.2302,0.0598+1j*0.1751],[0.0607+1j*0.2302,0.1939+1j*0.4885,0.0614+1j*0.1931],[0.0598+1j*0.1751,0.0614+1j*0.1931,0.1921+1j*0.4970]])
#print zseqs
#print zseql
#np.linalg.inv(np.matrix(zseqs))
#print np.linalg.inv(np.matrix(zseql))
yseqs=np.linalg.inv(np.matrix(zseqs))
yseql=np.linalg.inv(np.matrix(zseql))
print np.real(yseqs[0,1]),';',np.real(yseqs[0,2]),';',np.real(yseqs[1,2])
print np.real(yseqs[0,0]),';',np.real(yseqs[1,1]),';',np.real(yseqs[2,2])
print np.imag(yseqs[0,1]),';',np.real(yseqs[0,2]),';',np.real(yseqs[1,2])
print np.imag(yseqs[0,0]),';',np.real(yseqs[1,1]),';',np.real(yseqs[2,2])
print np.real(yseql[0,1]),';',np.real(yseql[0,2]),';',np.real(yseql[1,2])
print np.real(yseql[0,0]),';',np.real(yseql[1,1]),';',np.real(yseql[2,2])
print np.imag(yseql[0,1]),';',np.real(yseql[0,2]),';',np.real(yseql[1,2])
print np.imag(yseql[0,0]),';',np.real(yseql[1,1]),';',np.real(yseql[2,2])

print yseql
u=np.eye(3, 3)
A1=u
print A1
B1=zseqs
d1=u
A2=u
B2=zseql
d2=u
Zbase=2.4**2*1000/2000
Ztlow=(0.01+1j*0.06)*2.88

print 'ztrfm',1/Ztlow
Ztabc=np.matrix(np.array([[Ztlow,0.0,0.0],[0.0,Ztlow,0.0],[0.0,0.0,Ztlow]]))
nt=12.47/2.4
print nt,nt
At=1/nt*np.matrix(np.array([[1,0.0,-1],[-1,1,0.0],[0.0,-1,1]]))
Bt=Ztabc
dt=1/nt*np.matrix(np.array([[1,-1,0.0],[0.0,1,-1.0],[-1,0,1]]))
#define load
s4=np.matrix(np.array([[750*np.exp(1j*np.arccos(0.85))],[1000*np.exp(1j*np.arccos(0.9))],[1250*np.exp(1j*np.arccos(0.95))]]))
s4[0]=(6.38E+05+1j*3.95E+05)/1000.0
s4[1]=(9.00E+05+1j*4.36E+05)/1000.0
s4[2]=(1.19E+06+1j*3.90E+05)/1000.0

print np.abs(s4),np.rad2deg(np.angle(s4))
#define the infinite bus line-to-line neutral voltages
ELLs=np.matrix(np.array([[12470*np.exp(1j*np.deg2rad(30))],[12470*np.exp(1j*np.deg2rad(-90))],[12470*np.exp(1j*np.deg2rad(150))]]))
ELNs=np.matrix(np.array([[7199.6*np.exp(1j*np.deg2rad(0))],[7199.6*np.exp(1j*np.deg2rad(-120))],[7199.6*np.exp(1j*np.deg2rad(120))]]))
ELNs[0]=7.20E+03+1j*0.00E+00
ELNs[1]=-3.60E+03+1j*(-6.24E+03)
ELNs[2]=-3.60E+03+1j*6.24E+03

print 'ELNs',ELNs
V4=np.matrix(np.array([[2400*np.exp(1j*np.deg2rad(-30))],[2400*np.exp(1j*np.deg2rad(-150))],[2400*np.exp(1j*np.deg2rad(90))]]))
#initialization
I2=np.matrix(np.zeros((3,1)),'complex')
I3=np.matrix(np.zeros((3,1)),'complex')
#for i in range(len(s4)):
    #I3[i]=np.conj(s4[i]*(1000.0+0.0j)/V4[i])
#print np.abs(I3)
#print np.rad2deg(np.angle(I3))
Vold4=np.matrix(np.zeros((3,1)),'complex')
tol=0.5*1e-6
#print B1*I2
niter=0

V2=np.matrix(np.zeros((3,1)),'complex')
V2=ELNs
I3=np.matrix(np.zeros((3,1)),'complex')


degree=0
for j in range(3):
    ire=1000
    iim=2000         
    degree=degree-120
    I3[j]=ire+1j*iim
V3=At*V2-Bt*I3
print 'testV3',V3

while True:
    V2=A1*ELNs-B1*I2
    V3=At*V2-Bt*I3
    #print V3
    V4=A2*V3-B2*I3
    if niter==0:
        print 'V3',V3
        print 'V4',V4        
    if niter==1:
        print 'I3',I3
        print 'V2',V2
        print 'V3',V3
        print 'V4',V4
        
    #print np.max(np.abs(V4-Vold4))/2400.014
    if np.max(np.abs(V4-Vold4))/2400.0<tol or np.max(np.abs(V4-Vold4))/2400.0<tol:
        break
    for i in range(len(s4)):
        t=s4[i]*1000.0
        print 't',t
        #print t/V4[i]
        I3[i]=np.conj(t/V4[i])
    Vold4=V4
    I2=dt*I3
    niter=niter+1

print niter
print V4
print np.abs(V4)
print np.rad2deg(np.angle(V4))
#print At
#print Bt
#on 120v voltage Base
V4120=V4/2400*120
print np.abs(V4120)
print np.rad2deg(np.angle(V4120))
#the rated ct
Irated=6000/(np.sqrt(3)*2.4)
print 'irated',Irated
CT=1000/5
zeq=np.matrix(np.zeros((3,1),'complex'))
zsum=0.0+1j*0.0
for i in range(len(V4)):
    zeq[i]=(V3[i]-V4[i])/I3[i]
    zsum=zsum+zeq[i]
zaverage=zsum/3.0
print zaverage
#The value of the compensator impedances :
Rp=np.real(zaverage)*1000.0/20.0
Xp=np.imag(zaverage)*1000.0/20.0
print Rp,Xp
#the value of the compensator setting in ohm
Ro=Rp/5.0
Xo=Xp/5.0
PT=2400.0/120.0
Vreg=V3/PT
print np.abs(Vreg)
#the compensator currents
Icomp=I3/CT
Vrelay=np.matrix(np.zeros((3,1),'complex'))
for i in range(len(Vrelay)):
    Vrelay[i]=Vreg[i]-(Ro+1j*Xo)*Icomp[i]
print np.abs(Vrelay)
Tap=np.matrix(np.zeros((3,1)))
for i in range(len(V4)):
    Tap[i]=(120.0-np.abs(Vrelay[i]))/0.75
print Tap



