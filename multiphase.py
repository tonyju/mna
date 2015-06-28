import csv
from onephasepqbranch import onephasepqbranch
from threephaseconstantbranch import threephaseconstantbranch
from onephasetrfm import onephasetrfm
from onephaseregulator import onephaseregulator
from system import whole_system
from scipy.sparse import csr_matrix,coo_matrix,csc_matrix
from scipy.sparse import linalg

import scipy.sparse
import numpy as np
#print np.r_[[1,2],[2,3]]
#jacobian of pq elements
from sympy import *
from onephasevoltagesource import onephasevoltagesource

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

A1row=[]
A1col=[]
A1data=[]
A2row=[]
A2col=[]
A2data=[]
Grow=[]
Gcol=[]
Gdata=[]
Brow=[]
Bcol=[]
Bdata=[]
frerow=[]
frecol=[]
fredata=[]
fimrow=[]
fimcol=[]
fimdata=[]
#row = np.array([0, 0, 1, 2, 2, 2])
#col = np.array([0, 2, 2, 0, 1, 2])
#data = np.array([1, 2, 3, 4, 5, 6])
#print csr_matrix((data, (row, col)), shape=(3, 3)).toarray()
powsys=whole_system()
nodearray={}
#import system
i=0
nnode=0
n1branch=0
n2branch=0
with open('load.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    #print len(reader)
    for row in reader:
        if i==0:
            i=i+1
            continue
        onebranch=onephasepqbranch()
        onebranch.p=float(row[0])
        onebranch.q=float(row[1])
        onebranch.frnodename=row[2]
        onebranch.tonodename=row[3]
        if not nodearray.has_key(onebranch.frnodename) and not onebranch.frnodename=='-1':
            nodearray[onebranch.frnodename]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename) and not onebranch.tonodename=='-1':
            nodearray[onebranch.tonodename]=nnode
            nnode=nnode+1
        if onebranch.frnodename=='-1':
            nodearray[onebranch.frnodename]=-1
        if onebranch.tonodename=='-1':
            nodearray[onebranch.tonodename]=-1
        onebranch.frnode=nodearray[onebranch.frnodename]
        onebranch.tonode=nodearray[onebranch.tonodename]
        if not onebranch.frnode==-1:
            A2row.append(onebranch.frnode)
            A2col.append(n2branch)
            A2data.append(1.0)
        if not onebranch.tonode==-1:
            A2row.append(onebranch.tonode)
            A2col.append(n2branch)
            A2data.append(-1.0)        
        #print onebranch.frnode,onebranch.tonode
        #print onebranch.p
        onebranch.branchid=n2branch
        powsys.onephasepqbrancharray.append(onebranch)              
        n2branch=n2branch+1
        #print row[0],row[1],row[2],row[3],row[4],len(row)
i=0
with open('regulator.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    #print len(reader)
    for row in reader:
        if i==0:
            i=i+1
            continue
        onebranch=onephaseregulator()
        onebranch.frnodename[0]=row[0]
        onebranch.tonodename[0]=row[1]
        onebranch.frnodename[1]=row[2]
        onebranch.tonodename[1]=row[3]
        onebranch.ar=float(row[4])
        if not nodearray.has_key(onebranch.frnodename[0]) and not onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[0]) and not onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=-1
        if onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=-1
        onebranch.frnode[0]=nodearray[onebranch.frnodename[0]]
        onebranch.tonode[0]=nodearray[onebranch.tonodename[0]]
        if not onebranch.frnode[0]==-1:
            A2row.append(onebranch.frnode[0])
            A2col.append(n2branch)
            A2data.append(1.0)
        if not onebranch.tonode[0]==-1:
            A2row.append(onebranch.tonode[0])
            A2col.append(n2branch)
            A2data.append(-1.0)        
        #print onebranch.frnode,onebranch.tonode
        #print onebranch.p
        #rval[2*nnode+t.branchid]=0
        #rval[2*nnode+n2branch+t.branchid]=0
        onebranch.branchid[0]=n2branch 
        n2branch=n2branch+1
        
        if not nodearray.has_key(onebranch.frnodename[1]) and not onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[1]) and not onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=-1
        if onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=-1
        onebranch.frnode[1]=nodearray[onebranch.frnodename[1]]
        onebranch.tonode[1]=nodearray[onebranch.tonodename[1]]
        if not onebranch.frnode[1]==-1:
            A2row.append(onebranch.frnode[1])
            A2col.append(n2branch)
            A2data.append(1.0)
        if not onebranch.tonode[1]==-1:
            A2row.append(onebranch.tonode[1])
            A2col.append(n2branch)
            A2data.append(-1.0)        
        #print onebranch.frnode,onebranch.tonode
        #print onebranch.p
        onebranch.branchid[1]=n2branch            
        n2branch=n2branch+1        
        powsys.onephaseregulatorarray.append(onebranch)              
        #print row[0],row[1],row[2],row[3],row[4],len(row)      
i=0
with open('voltagesource.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    #print len(reader)
    for row in reader:
        if i==0:
            i=i+1
            continue
        onebranch=onephasevoltagesource()
        onebranch.vre=float(row[2])
        onebranch.vim=float(row[3])
        onebranch.frnodename=row[0]
        onebranch.tonodename=row[1]
        if not nodearray.has_key(onebranch.frnodename) and not onebranch.frnodename=='-1':
            nodearray[onebranch.frnodename]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename) and not onebranch.tonodename=='-1':
            nodearray[onebranch.tonodename]=nnode
            nnode=nnode+1
        if onebranch.frnodename=='-1':
            nodearray[onebranch.frnodename]=-1
        if onebranch.tonodename=='-1':
            nodearray[onebranch.tonodename]=-1
        onebranch.frnode=nodearray[onebranch.frnodename]
        onebranch.tonode=nodearray[onebranch.tonodename]
        if not onebranch.frnode==-1:
            A2row.append(onebranch.frnode)
            A2col.append(n2branch)
            A2data.append(1.0)
        if not onebranch.tonode==-1:
            A2row.append(onebranch.tonode)
            A2col.append(n2branch)
            A2data.append(-1.0)        
        #print onebranch.frnode,onebranch.tonode
        #print onebranch.p
        #frerow.append(n2branch)
        #frecol.append(onebranch.frnode)
        #fredata.append(1.0)
        onebranch.branchid=n2branch
        powsys.onephasevoltagesourcearray.append(onebranch)
        n2branch=n2branch+1
        #print row[0],row[1],row[2],row[3],row[4],len(row)

i=0
with open('acline.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    #print len(reader)
    for row in reader:
        if i==0:
            i=i+1
            print row
            continue
        onebranch=threephaseconstantbranch()
        #the output file position [0,1][0,2],[1,0],[1,2],[2,0],[2,1]
        #                           0,  1,     2,   3,     4,   5
        srow=row[0].split(';')
        #print srow
        onebranch.offdiagg[0]=float(srow[0])#the input file position [0,1][0,2],[1,2]
        onebranch.offdiagg[2]=float(srow[0])
        onebranch.offdiagg[1]=float(srow[1])
        onebranch.offdiagg[4]=float(srow[1])
        onebranch.offdiagg[3]=float(srow[2])
        onebranch.offdiagg[5]=float(srow[2])
        srow=row[1].split(';')
        onebranch.diagg[0]=float(srow[0])
        onebranch.diagg[1]=float(srow[1])
        onebranch.diagg[2]=float(srow[2])
        srow=row[2].split(';')
        #print srow
        onebranch.offdiagb[0]=float(srow[0])#the input file position [0,1][0,2],[1,2]
        onebranch.offdiagb[2]=float(srow[0])
        onebranch.offdiagb[1]=float(srow[1])
        onebranch.offdiagb[4]=float(srow[1])
        onebranch.offdiagb[3]=float(srow[2])
        onebranch.offdiagb[5]=float(srow[2])
        srow=row[3].split(';')
        onebranch.diagb[0]=float(srow[0])
        onebranch.diagb[1]=float(srow[1])
        onebranch.diagb[2]=float(srow[2])
        srow=row[4].split(';')
        onebranch.frnodename[0]=srow[1]
        onebranch.frnodename[1]=srow[2]
        onebranch.frnodename[2]=srow[3]
        srow=row[5].split(';')
        onebranch.tonodename[0]=srow[1]
        onebranch.tonodename[1]=srow[2]
        onebranch.tonodename[2]=srow[3]
        if not nodearray.has_key(onebranch.frnodename[0]) and not onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[0]) and not onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=-1
        if onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=-1
        onebranch.frnode[0]=nodearray[onebranch.frnodename[0]]
        onebranch.tonode[0]=nodearray[onebranch.tonodename[0]]
        if not onebranch.frnode[0]==-1:
            A1row.append(onebranch.frnode[0])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode==-1:
            A1row.append(onebranch.tonode[0])
            A1col.append(n1branch)
            A1data.append(-1.0)
        n1branch=n1branch+1        
        if not nodearray.has_key(onebranch.frnodename[1]) and not onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[1]) and not onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=-1
        if onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=-1
        onebranch.frnode[1]=nodearray[onebranch.frnodename[1]]
        onebranch.tonode[1]=nodearray[onebranch.tonodename[1]]
        if not onebranch.frnode[1]==-1:
            A1row.append(onebranch.frnode[1])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[1]==-1:
            A1row.append(onebranch.tonode[1])
            A1col.append(n1branch)
            A1data.append(-1.0)
        n1branch=n1branch+1
        if not nodearray.has_key(onebranch.frnodename[2]) and not onebranch.frnodename[2]=='-1':
            nodearray[onebranch.frnodename[2]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[2]) and not onebranch.tonodename[2]=='-1':
            nodearray[onebranch.tonodename[2]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[2]=='-1':
            nodearray[onebranch.frnodename[2]]=-1
        if onebranch.tonodename[2]=='-1':
            nodearray[onebranch.tonodename[2]]=-1
        onebranch.frnode[2]=nodearray[onebranch.frnodename[2]]
        onebranch.tonode[2]=nodearray[onebranch.tonodename[2]]
        if not onebranch.frnode[2]==-1:
            A1row.append(onebranch.frnode[2])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[2]==-1:
            A1row.append(onebranch.tonode[2])
            A1col.append(n1branch)
            A1data.append(-1.0)
        Grow.append(n1branch-2)
        Gcol.append(n1branch-2)
        Gdata.append(onebranch.diagg[0])
        Grow.append(n1branch-1)
        Gcol.append(n1branch-1)
        Gdata.append(onebranch.diagg[1])        
        Grow.append(n1branch-0)
        Gcol.append(n1branch-0)
        Gdata.append(onebranch.diagg[2])
        #[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]
        Grow.append(n1branch-2)
        Gcol.append(n1branch-1)
        Gdata.append(onebranch.offdiagg[0])
        Grow.append(n1branch-2)
        Gcol.append(n1branch)
        Gdata.append(onebranch.offdiagg[1])
        Grow.append(n1branch-1)
        Gcol.append(n1branch-2)
        Gdata.append(onebranch.offdiagg[2])
        Grow.append(n1branch-1)
        Gcol.append(n1branch)
        Gdata.append(onebranch.offdiagg[3])
        Grow.append(n1branch)
        Gcol.append(n1branch-2)
        Gdata.append(onebranch.offdiagg[4])
        Grow.append(n1branch)
        Gcol.append(n1branch-1)
        Gdata.append(onebranch.offdiagg[5])        
                        
        Brow.append(n1branch-2)
        Bcol.append(n1branch-2)
        Bdata.append(onebranch.diagb[0])
        Brow.append(n1branch-1)
        Bcol.append(n1branch-1)
        Bdata.append(onebranch.diagb[1])        
        Brow.append(n1branch-0)
        Bcol.append(n1branch-0)
        Bdata.append(onebranch.diagb[2])        
        #[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]
        Brow.append(n1branch-2)
        Bcol.append(n1branch-1)
        Bdata.append(onebranch.offdiagb[0])
        Brow.append(n1branch-2)
        Bcol.append(n1branch)
        Bdata.append(onebranch.offdiagb[1])
        Brow.append(n1branch-1)
        Bcol.append(n1branch-2)
        Bdata.append(onebranch.offdiagb[2])
        Brow.append(n1branch-1)
        Bcol.append(n1branch)
        Bdata.append(onebranch.offdiagb[3])
        Brow.append(n1branch)
        Bcol.append(n1branch-2)
        Bdata.append(onebranch.offdiagb[4])
        Brow.append(n1branch)
        Bcol.append(n1branch-1)
        Bdata.append(onebranch.offdiagb[5])   
             
        n1branch=n1branch+1
        powsys.threephaseconstantbrancharray.append(onebranch)
#print nodearray
i=0
with open('trfmwinding.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    #print len(reader)
    for row in reader:
        if i==0:
            i=i+1
            continue
        if row[0]=='':
            continue
        print row
        srow1=row[0].split(';')
        srow2=row[1].split(';')
        srow3=row[2].split(';')
        srow4=row[3].split(';')
        srow5=row[4].split(';')
        ratio=float(row[5])
        #three coupling
        #1
        onebranch=onephasetrfm()
        onebranch.g=float(srow1[1])
        onebranch.b=float(srow2[1])
        if srow5[0]=='1' :#Y connection
            onebranch.frnodename[0]=srow3[1]
            onebranch.tonodename[0]='trfm-'+str(i)+'-neutral'
        if srow5[1]=='0':#D connection
            onebranch.frnodename[1]=srow4[1]
            onebranch.tonodename[1]=srow4[2]
        if srow5[0]=='0' :#D connection
            onebranch.frnodename[0]=srow3[1]
            onebranch.tonodename[0]=srow3[2]
        if srow5[1]=='1':#Y connection
            onebranch.frnodename[1]=srow4[2]
            onebranch.tonodename[1]='trfm-'+str(i)+'-neutral'
        onebranch.kre=ratio
        onebranch.kim=0.0
        
        if not nodearray.has_key(onebranch.frnodename[0]) and not onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[0]) and not onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=-1
        if onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=-1
        onebranch.frnode[0]=nodearray[onebranch.frnodename[0]]
        onebranch.tonode[0]=nodearray[onebranch.tonodename[0]]
        if not onebranch.frnode[0]==-1:
            A1row.append(onebranch.frnode[0])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[0]==-1:
            A1row.append(onebranch.tonode[0])
            A1col.append(n1branch)
            A1data.append(-1.0)
        n1branch=n1branch+1
        
        if not nodearray.has_key(onebranch.frnodename[1]) and not onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[1]) and not onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=-1
        if onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=-1
        onebranch.frnode[1]=nodearray[onebranch.frnodename[1]]
        onebranch.tonode[1]=nodearray[onebranch.tonodename[1]]
        if not onebranch.frnode[1]==-1:
            A1row.append(onebranch.frnode[1])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[1]==-1:
            A1row.append(onebranch.tonode[1])
            A1col.append(n1branch)
            A1data.append(-1.0)
        
        y=onebranch.g+1j*onebranch.b
        alphav=onebranch.kre+1j*onebranch.kim
        alphai=onebranch.kre-1j*onebranch.kim
        g00=np.real(y/(alphav*alphai))
        b00=np.imag(y/(alphav*alphai))
        g01=np.real(-y/alphai)
        b01=np.imag(-y/alphai)
        g10=np.real(-y/alphav)
        b10=np.imag(-y/alphav)
        g11=np.real(y)
        b11=np.imag(y)
        Grow.append(n1branch)
        Gcol.append(n1branch)
        Gdata.append(g11)
        Grow.append(n1branch-1)
        Gcol.append(n1branch-1)
        Gdata.append(g00)
        Grow.append(n1branch-1)
        Gcol.append(n1branch)
        Gdata.append(g01)
        Grow.append(n1branch)
        Gcol.append(n1branch-1)
        Gdata.append(g10)
        Brow.append(n1branch)
        Bcol.append(n1branch)
        Bdata.append(b11)
        Brow.append(n1branch-1)
        Bcol.append(n1branch-1)
        Bdata.append(b00)
        Brow.append(n1branch-1)
        Bcol.append(n1branch)
        Bdata.append(b01)
        Brow.append(n1branch)
        Bcol.append(n1branch-1)
        Bdata.append(b10)                              
        
        n1branch=n1branch+1
        powsys.onephasetrfmarray.append(onebranch)
        #2
        onebranch=onephasetrfm()
        onebranch.g=float(srow1[3])
        onebranch.b=float(srow2[3])
        if srow5[0]=='1' :#Y connection
            onebranch.frnodename[0]=srow3[2]
            onebranch.tonodename[0]='trfm-'+str(i)+'-neutral'
        if srow5[1]=='0':#D connection
            onebranch.frnodename[1]=srow4[2]
            onebranch.tonodename[1]=srow4[3]
        if srow5[0]=='0' :#D connection
            onebranch.frnodename[0]=srow3[2]
            onebranch.tonodename[0]=srow3[3]
        if srow5[1]=='1':#Y connection
            onebranch.frnodename[1]=srow4[3]
            onebranch.tonodename[1]='trfm-'+str(i)+'-neutral'
        onebranch.kre=ratio
        onebranch.kim=0.0
        if not nodearray.has_key(onebranch.frnodename[0]) and not onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[0]) and not onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=-1
        if onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=-1
        onebranch.frnode[0]=nodearray[onebranch.frnodename[0]]
        onebranch.tonode[0]=nodearray[onebranch.tonodename[0]]
        if not onebranch.frnode[0]==-1:
            A1row.append(onebranch.frnode[0])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[0]==-1:
            A1row.append(onebranch.tonode[0])
            A1col.append(n1branch)
            A1data.append(-1.0)
        n1branch=n1branch+1        
        if not nodearray.has_key(onebranch.frnodename[1]) and not onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[1]) and not onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=-1
        if onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=-1
        onebranch.frnode[1]=nodearray[onebranch.frnodename[1]]
        onebranch.tonode[1]=nodearray[onebranch.tonodename[1]]
        if not onebranch.frnode[1]==-1:
            A1row.append(onebranch.frnode[1])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[1]==-1:
            A1row.append(onebranch.tonode[1])
            A1col.append(n1branch)
            A1data.append(-1.0)
        y=onebranch.g+1j*onebranch.b
        alphav=onebranch.kre+1j*onebranch.kim
        alphai=onebranch.kre-1j*onebranch.kim
        g00=np.real(y/(alphav*alphai))
        b00=np.imag(y/(alphav*alphai))
        g01=np.real(-y/alphai)
        b01=np.imag(-y/alphai)
        g10=np.real(-y/alphav)
        b10=np.imag(-y/alphav)
        g11=np.real(y)
        b11=np.imag(y)
        Grow.append(n1branch)
        Gcol.append(n1branch)
        Gdata.append(g11)
        Grow.append(n1branch-1)
        Gcol.append(n1branch-1)
        Gdata.append(g00)
        Grow.append(n1branch-1)
        Gcol.append(n1branch)
        Gdata.append(g01)
        Grow.append(n1branch)
        Gcol.append(n1branch-1)
        Gdata.append(g10)
        Brow.append(n1branch)
        Bcol.append(n1branch)
        Bdata.append(b11)
        Brow.append(n1branch-1)
        Bcol.append(n1branch-1)
        Bdata.append(b00)
        Brow.append(n1branch-1)
        Bcol.append(n1branch)
        Bdata.append(b01)
        Brow.append(n1branch)
        Bcol.append(n1branch-1)
        Bdata.append(b10)

        n1branch=n1branch+1                
        powsys.onephasetrfmarray.append(onebranch)
        #3
        onebranch=onephasetrfm()
        onebranch.g=float(srow1[5])
        onebranch.b=float(srow2[5])
        if srow5[0]=='1' :#Y connection
            onebranch.frnodename[0]=srow3[3]
            onebranch.tonodename[0]='trfm-'+str(i)+'-neutral'
        if srow5[1]=='0':#D connection
            onebranch.frnodename[1]=srow4[3]
            onebranch.tonodename[1]=srow4[1]
        if srow5[0]=='0' :#D connection
            onebranch.frnodename[0]=srow3[3]
            onebranch.tonodename[0]=srow3[1]
        if srow5[1]=='1':#Y connection
            onebranch.frnodename[1]=srow4[1]
            onebranch.tonodename[1]='trfm-'+str(i)+'-neutral'
        onebranch.kre=ratio
        onebranch.kim=0.0
        if not nodearray.has_key(onebranch.frnodename[0]) and not onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[0]) and not onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[0]=='-1':
            nodearray[onebranch.frnodename[0]]=-1
        if onebranch.tonodename[0]=='-1':
            nodearray[onebranch.tonodename[0]]=-1
        onebranch.frnode[0]=nodearray[onebranch.frnodename[0]]
        onebranch.tonode[0]=nodearray[onebranch.tonodename[0]]
        if not onebranch.frnode[0]==-1:
            A1row.append(onebranch.frnode[0])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[0]==-1:
            A1row.append(onebranch.tonode[0])
            A1col.append(n1branch)
            A1data.append(-1.0)
        n1branch=n1branch+1
        if not nodearray.has_key(onebranch.frnodename[1]) and not onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=nnode
            nnode=nnode+1
        if not nodearray.has_key(onebranch.tonodename[1]) and not onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=nnode
            nnode=nnode+1
        if onebranch.frnodename[1]=='-1':
            nodearray[onebranch.frnodename[1]]=-1
        if onebranch.tonodename[1]=='-1':
            nodearray[onebranch.tonodename[1]]=-1
        onebranch.frnode[1]=nodearray[onebranch.frnodename[1]]
        onebranch.tonode[1]=nodearray[onebranch.tonodename[1]]        
        if not onebranch.frnode[1]==-1:
            A1row.append(onebranch.frnode[1])
            A1col.append(n1branch)
            A1data.append(1.0)
        if not onebranch.tonode[1]==-1:
            A1row.append(onebranch.tonode[1])
            A1col.append(n1branch)
            A1data.append(-1.0)
        y=onebranch.g+1j*onebranch.b
        alphav=onebranch.kre+1j*onebranch.kim
        alphai=onebranch.kre-1j*onebranch.kim
        g00=np.real(y/(alphav*alphai))
        b00=np.imag(y/(alphav*alphai))
        g01=np.real(-y/alphai)
        b01=np.imag(-y/alphai)
        g10=np.real(-y/alphav)
        b10=np.imag(-y/alphav)
        g11=np.real(y)
        b11=np.imag(y)
        Grow.append(n1branch)
        Gcol.append(n1branch)
        Gdata.append(g11)
        Grow.append(n1branch-1)
        Gcol.append(n1branch-1)
        Gdata.append(g00)
        Grow.append(n1branch-1)
        Gcol.append(n1branch)
        Gdata.append(g01)
        Grow.append(n1branch)
        Gcol.append(n1branch-1)
        Gdata.append(g10)
        Brow.append(n1branch)
        Bcol.append(n1branch)
        Bdata.append(b11)
        Brow.append(n1branch-1)
        Bcol.append(n1branch-1)
        Bdata.append(b00)
        Brow.append(n1branch-1)
        Bcol.append(n1branch)
        Bdata.append(b01)
        Brow.append(n1branch)
        Bcol.append(n1branch-1)
        Bdata.append(b10)

        n1branch=n1branch+1        
        powsys.onephasetrfmarray.append(onebranch)        
        #onebranch.p=float(row[0])
        #onebranch.q=float(row[1])
        #onebranch.frnodename=row[2]
        #onebranch.tonodename=row[3]
        #print onebranch.p
        #powsys.onephasepqbrancharray.append(onebranch)
        #print row[0],row[1],row[2],row[3],row[4],len(row)
#print nodearray
#antifloating add reference bus to winding neutral

onebranch=onephasevoltagesource()
onebranch.frnodename='trfm-'+'1'+'-neutral'
onebranch.tonodename='-1'
onebranch.vre=0.0
onebranch.vim=0.0
if not nodearray.has_key(onebranch.frnodename) and not onebranch.frnodename=='-1':
    nodearray[onebranch.frnodename]=nnode
    nnode=nnode+1
if not nodearray.has_key(onebranch.tonodename) and not onebranch.tonodename=='-1':
    nodearray[onebranch.tonodename]=nnode
    nnode=nnode+1
if onebranch.frnodename=='-1':
    nodearray[onebranch.frnodename]=-1
if onebranch.tonodename=='-1':
    nodearray[onebranch.tonodename]=-1
onebranch.frnode=nodearray[onebranch.frnodename]
onebranch.tonode=nodearray[onebranch.tonodename]
if not onebranch.frnode==-1:
    A2row.append(onebranch.frnode)
    A2col.append(n2branch)
    A2data.append(1.0)
if not onebranch.tonode==-1:
    A2row.append(onebranch.tonode)
    A2col.append(n2branch)
    A2data.append(-1.0)        
#print onebranch.frnode,onebranch.tonode
#print onebranch.p
#frerow.append(n2branch)
#frecol.append(onebranch.frnode)
#fredata.append(1.0)
onebranch.branchid=n2branch
powsys.onephasevoltagesourcearray.append(onebranch)
n2branch=n2branch+1
#print row[0],row[1],row[2],row[3],row[4],len(row)


rval=[]
for i in range(2*nnode+2*n2branch):
    rval.append(0.0)
#print np.r_[rval]
    #for modified nodal analysis method,first the node index
for j in range(len(powsys.onephasevoltagesourcearray)):
    t=onephasevoltagesource()
    t=powsys.onephasevoltagesourcearray[j]
    if not t.frnode==-1:
        frerow.append(t.branchid)
        frecol.append(t.frnode)
        fredata.append(1.0)
    if not t.tonode==-1:#-1 means grounded node
        frerow.append(t.branchid)
        frecol.append(t.tonode)
        fredata.append(-1.0)
    if not t.frnode==-1:
        fimrow.append(t.branchid)
        fimcol.append(t.frnode+nnode)
        fimdata.append(1.0)
    if not t.tonode==-1:
        fimrow.append(t.branchid)
        fimcol.append(t.tonode+nnode)
        fimdata.append(-1.0)
    print t.branchid
    rval[2*nnode+t.branchid]=t.vre
    rval[2*nnode+n2branch+t.branchid]=t.vim
for j in range(len(powsys.onephasepqbrancharray)):
    t=onephasepqbranch()
    t=powsys.onephasepqbrancharray[j]
    frerow.append(t.branchid)
    frecol.append(t.branchid+2*nnode)
    fredata.append(1.0)
    
    fimrow.append(t.branchid)
    fimcol.append(t.branchid+n2branch+2*nnode)
    fimdata.append(1.0)
    rval[2*nnode+t.branchid]=t.ire
    rval[2*nnode+n2branch+t.branchid]=t.iim          
    print t.branchid
for j in range(len(powsys.onephaseregulatorarray)):
    onebranch=onephaseregulator()
    onebranch=powsys.onephaseregulatorarray[j]
    if not onebranch.frnode[0]==-1:
        frerow.append(onebranch.branchid[0])
        frecol.append(onebranch.frnode[0])
        fredata.append(1.0)
    if not onebranch.tonode[0]==-1:
        frerow.append(onebranch.branchid[0])
        frecol.append(onebranch.tonode[0])
        fredata.append(-1.0)
    if not onebranch.frnode[1]==-1:
        frerow.append(onebranch.branchid[0])
        frecol.append(onebranch.frnode[1])
        fredata.append(-onebranch.ar)
    if not onebranch.tonode[1]==-1:
        frerow.append(onebranch.branchid[0])
        frecol.append(onebranch.tonode[1])
        fredata.append(onebranch.ar)        
    
    if not onebranch.frnode[0]==-1:
        fimrow.append(onebranch.branchid[0])
        fimcol.append(onebranch.frnode[0]+nnode)
        fimdata.append(1.0)
    if not onebranch.tonode==-1:
        fimrow.append(onebranch.branchid[0])
        fimcol.append(onebranch.tonode[0]+nnode)
        fimdata.append(-1.0)
    if not onebranch.frnode[1]==-1:
        fimrow.append(onebranch.branchid[0])
        fimcol.append(onebranch.frnode[1]+nnode)
        fimdata.append(-onebranch.ar)
    if not onebranch.tonode[1]==-1:
        fimrow.append(onebranch.branchid[0])
        fimcol.append(onebranch.tonode[1]+nnode)
        fimdata.append(onebranch.ar)
    
    frerow.append(onebranch.branchid[1])
    frecol.append(onebranch.branchid[1]+2*nnode)
    fredata.append(1.0)        
    frerow.append(onebranch.branchid[1])
    frecol.append(onebranch.branchid[0]+2*nnode)
    fredata.append(onebranch.ar)
    
    fimrow.append(onebranch.branchid[1])
    fimcol.append(onebranch.branchid[1]+2*nnode+n2branch)
    fimdata.append(1.0)        
    fimrow.append(onebranch.branchid[1])
    fimcol.append(onebranch.branchid[0]+2*nnode+n2branch)
    fimdata.append(onebranch.ar) 

row = np.array(A1row)
col = np.array(A1col)
data = np.array(A1data)
A1=csr_matrix((data, (row, col)), shape=(nnode,n1branch))
row = np.array(A1col)
col = np.array(A1row)
data = np.array(A1data)
A1T=csr_matrix((data, (row, col)), shape=(n1branch,nnode))

row = np.array(A2row)
col = np.array(A2col)
data = np.array(A2data)
A2=csr_matrix((data, (row, col)), shape=(nnode,n2branch))

row = np.array(Grow)
col = np.array(Gcol)
data = np.array(Gdata)
G=csr_matrix((data, (row, col)), shape=(n1branch,n1branch))

row = np.array(frerow)
col = np.array(frecol)
data = np.array(fredata)
fre=csr_matrix((data, (row, col)), shape=(n2branch,2*n2branch+2*nnode))

row = np.array(fimrow)
col = np.array(fimcol)
data = np.array(fimdata)
fim=csr_matrix((data, (row, col)), shape=(n2branch,2*n2branch+2*nnode))

row = np.array(Brow)
col = np.array(Bcol)
data = np.array(Bdata)
B=csr_matrix((data, (row, col)), shape=(n1branch,n1branch))


C=A1*G*A1T
#print scipy.sparse.linalg.factorized(C)
#r_[,,]
F=np.r_[rval]
#
A2diag=scipy.sparse.block_diag((A2, A2))
#print A2diag
J11 = scipy.sparse.vstack([
                scipy.sparse.hstack([A1*G*A1T, -A1*B*A1T]),
                scipy.sparse.hstack([A1*B*A1T, A1*G*A1T])
            ], format="csr")
Jup=scipy.sparse.hstack([J11,A2diag],format="csr")
J=scipy.sparse.vstack([Jup,fre,fim],format="csr")

mat=np.matrix(A2diag.todense())
np.savetxt('text.txt',mat,fmt='%.2f')
dx=linalg.spsolve(J, F)


print '1a',dx[nodearray['1a']]+1j*dx[nodearray['1a']+nnode]
print '1b',dx[nodearray['1b']]+1j*dx[nodearray['1b']+nnode]
print '1c',dx[nodearray['1c']]+1j*dx[nodearray['1c']+nnode]
print '2a',dx[nodearray['2a']]+1j*dx[nodearray['2a']+nnode]
print '2b',dx[nodearray['2b']]+1j*dx[nodearray['2b']+nnode]
print '2c',dx[nodearray['2c']]+1j*dx[nodearray['2c']+nnode]
print '3a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]
print '3b',dx[nodearray['3b']]+1j*dx[nodearray['3b']+nnode]
print '3c',dx[nodearray['3c']]+1j*dx[nodearray['3c']+nnode]
print '3ar',dx[nodearray['3ar']]+1j*dx[nodearray['3ar']+nnode]
print '3br',dx[nodearray['3br']]+1j*dx[nodearray['3br']+nnode]
print '3cr',dx[nodearray['3cr']]+1j*dx[nodearray['3cr']+nnode]

print '4a',dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
print '4b',dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
print '4c',dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]

for iter in range(8):   
    for j in range(len(powsys.onephasepqbrancharray)):
        t=onephasepqbranch()
        t=powsys.onephasepqbrancharray[j]
        t.ire=np.real((t.p+1j*t.q)/(dx[t.frnode]+1j*dx[t.frnode+nnode]))
        t.iim=-np.imag((t.p+1j*t.q)/(dx[t.frnode]+1j*dx[t.frnode+nnode]))
        if iter==0:
            #print t.ire
            #print t.iim
            ival=t.ire+1j*t.iim
            sval=t.p+1j*t.q
            vval=dx[t.frnode]+1j*dx[t.frnode+nnode]
            #print vval
            #print t.frnode
            #print t.frnodename
            #print nodearray['4c']
            #print 'i',ival
            #print 'v',vval
            #print 's',sval
            #print 'i',np.abs(ival),'<',np.rad2deg(np.angle(ival))
            #print 's',np.abs(sval),'<',np.rad2deg(np.angle(sval))
            #print 'v',np.abs(vval),'<',np.rad2deg(np.angle(vval))
            #print vval
        rval[2*nnode+t.branchid]=t.ire
        rval[2*nnode+n2branch+t.branchid]=t.iim
    F=np.r_[rval]
    if iter==1:
        pass
        #print 'iter=1,v4a',dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
        #print 'iter=1,v3a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]
        #print 'iter=1,v34a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]-(dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode])
        #print 'iter=1,v4b',dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
        #print 'iter=1,v4c',dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]
        #print 'i1a',(dx[2*nnode]+1j*dx[2*nnode+n2branch]) 
        #v4a=dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
        #print 'v4a',np.abs(v4a),np.angle(v4a)
        #print 'rval',F        
    dx=linalg.spsolve(J, F)
print '1a',dx[nodearray['1a']]+1j*dx[nodearray['1a']+nnode]
print '1b',dx[nodearray['1b']]+1j*dx[nodearray['1b']+nnode]
print '1c',dx[nodearray['1c']]+1j*dx[nodearray['1c']+nnode]
print '2a',dx[nodearray['2a']]+1j*dx[nodearray['2a']+nnode]
print '2b',dx[nodearray['2b']]+1j*dx[nodearray['2b']+nnode]
print '2c',dx[nodearray['2c']]+1j*dx[nodearray['2c']+nnode]
print '3a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]
print '3b',dx[nodearray['3b']]+1j*dx[nodearray['3b']+nnode]
print '3c',dx[nodearray['3c']]+1j*dx[nodearray['3c']+nnode]
print '3ar',dx[nodearray['3ar']]+1j*dx[nodearray['3ar']+nnode]
print '3br',dx[nodearray['3br']]+1j*dx[nodearray['3br']+nnode]
print '3cr',dx[nodearray['3cr']]+1j*dx[nodearray['3cr']+nnode]
print '4a',dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
print '4b',dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
print '4c',dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]
#print 'v34a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]-(dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode])
v4a=dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
v4b=dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
v4c=dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]
print 'v4a',np.abs(v4a),np.rad2deg(np.angle(v4a))
print 'v4b',np.abs(v4b),np.rad2deg(np.angle(v4b))
print 'v4c',np.abs(v4c),np.rad2deg(np.angle(v4c))
print 'i1a',(dx[2*nnode]+1j*dx[2*nnode+n2branch])
print 's1a',(dx[2*nnode]-1j*dx[2*nnode+n2branch])*(dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode])

print 'i1b',dx[2*nnode+1]+1j*dx[2*nnode+n2branch+1]
print 's1b',(dx[2*nnode+1]-1j*dx[2*nnode+n2branch+1])*(dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode])

print 'i1c',dx[2*nnode+2]+1j*dx[2*nnode+n2branch+2]
print 's1c',(dx[2*nnode+2]-1j*dx[2*nnode+n2branch+2])*(dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode])

print 'i2ar',dx[2*nnode+3]+1j*dx[2*nnode+n2branch+3]
print 'i2br',dx[2*nnode+5]+1j*dx[2*nnode+n2branch+5]
print 'i2cr',dx[2*nnode+7]+1j*dx[2*nnode+n2branch+7]

print 'i2a',dx[2*nnode+4]+1j*dx[2*nnode+n2branch+4]
print 'i2b',dx[2*nnode+6]+1j*dx[2*nnode+n2branch+6]
print 'i2c',dx[2*nnode+8]+1j*dx[2*nnode+n2branch+8]



#print dx[2*nnode+3]+1j*dx[2*nnode+n2branch+3]+dx[2*nnode+4]+1j*dx[2*nnode+n2branch+4]+dx[2*nnode+5]+1j*dx[2*nnode+n2branch+5]
v3=np.array([[dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]],[dx[nodearray['3b']]+1j*dx[nodearray['3b']+nnode]],[dx[nodearray['3c']]+1j*dx[nodearray['3c']+nnode]]])
v3=np.matrix(v3)
v4=np.array([[dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]],[dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]],[dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]]])
v4=np.matrix(v4)
i3comp=np.matrix(np.zeros((3,1),'complex'))
v3comp=np.matrix(np.zeros((3,1),'complex'))
vreg=np.matrix(np.zeros((3,1),'complex'))
vrelay=np.matrix(np.zeros((3,1),'complex'))
tap=np.matrix(np.zeros((3,1)))
for nreg in range(len(powsys.onephaseregulatorarray)):
    reg=onephaseregulator()
    reg=powsys.onephaseregulatorarray[nreg]
    if nreg==0:
        reg.tap0=20
    if nreg==1:
        reg.tap0=0
    if nreg==2:
        reg.tap0=15
xiter=[]
y={}
y['0']=[]
y['1']=[]
y['2']=[]               
for nregiter in range(18):
    frerow=[]
    frecol=[]
    fredata=[]
    fimrow=[]
    fimcol=[]
    fimdata=[]
    for j in range(len(powsys.onephasevoltagesourcearray)):
        t=onephasevoltagesource()
        t=powsys.onephasevoltagesourcearray[j]
        if not t.frnode==-1:
            frerow.append(t.branchid)
            frecol.append(t.frnode)
            fredata.append(1.0)
        if not t.tonode==-1:
            frerow.append(t.branchid)
            frecol.append(t.tonode)
            fredata.append(-1.0)
        if not t.frnode==-1:
            fimrow.append(t.branchid)
            fimcol.append(t.frnode+nnode)
            fimdata.append(1.0)
        if not t.tonode==-1:
            fimrow.append(t.branchid)
            fimcol.append(t.tonode+nnode)
            fimdata.append(-1.0)
        #print t.branchid
        rval[2*nnode+t.branchid]=t.vre
        rval[2*nnode+n2branch+t.branchid]=t.vim
    for j in range(len(powsys.onephasepqbrancharray)):
        t=onephasepqbranch()
        t=powsys.onephasepqbrancharray[j]
        frerow.append(t.branchid)
        frecol.append(t.branchid+2*nnode)
        fredata.append(1.0)
        
        fimrow.append(t.branchid)
        fimcol.append(t.branchid+n2branch+2*nnode)
        fimdata.append(1.0)
        rval[2*nnode+t.branchid]=t.ire
        rval[2*nnode+n2branch+t.branchid]=t.iim          
        #print t.branchid

    for nreg in range(len(powsys.onephaseregulatorarray)):
        reg=onephaseregulator()
        reg=powsys.onephaseregulatorarray[nreg]
        i3comp[nreg]=-(dx[2*nnode+reg.branchid[1]]+1j*dx[2*nnode+n2branch+reg.branchid[1]])/reg.ct
        vreg[nreg]=(dx[reg.frnode[1]]+1j*dx[reg.frnode[1]+nnode])/reg.pt
        v3comp[nreg]=i3comp[nreg]*(reg.rcomp+1j*reg.xcomp)
        vrelay[nreg]=vreg[nreg]-v3comp[nreg]
        if np.abs(vrelay[nreg])<120.0+0.5*reg.bandwidth and np.abs(vrelay[nreg])>120.0-0.5*reg.bandwidth:
            print np.abs(vrelay[nreg]),reg.frnodename[1],'already in bandwidth'
        else:
            print np.abs(vrelay[nreg]),'not in bandwidth'
            if nregiter==0:
                tap[nreg]=round((reg.voltagelevel-np.abs(vrelay[nreg]))/0.75)
                reg.tap=tap[nreg]
                #reg.tap0=reg.tap
                reg.ar=1-0.00625*tap[nreg]
            else:
                deltatap=round((reg.voltagelevel-np.abs(vrelay[nreg]))/0.75)
                tap[nreg]=reg.tap+deltatap
                if tap[nreg]>20:
                    tap[nreg]=20.0
                reg.ar=1-0.00625*tap[nreg]
        onebranch=onephaseregulator()
        onebranch=powsys.onephaseregulatorarray[nreg]
        if not onebranch.frnode[0]==-1:
            frerow.append(onebranch.branchid[0])
            frecol.append(onebranch.frnode[0])
            fredata.append(1.0)
        if not onebranch.tonode[0]==-1:
            frerow.append(onebranch.branchid[0])
            frecol.append(onebranch.tonode[0])
            fredata.append(-1.0)
        if not onebranch.frnode[1]==-1:
            frerow.append(onebranch.branchid[0])
            frecol.append(onebranch.frnode[1])
            fredata.append(-onebranch.ar)
        if not onebranch.tonode[1]==-1:
            frerow.append(onebranch.branchid[0])
            frecol.append(onebranch.tonode[1])
            fredata.append(onebranch.ar)
        #print onebranch.frnodename[1],onebranch.ar        
        
        if not onebranch.frnode[0]==-1:
            fimrow.append(onebranch.branchid[0])
            fimcol.append(onebranch.frnode[0]+nnode)
            fimdata.append(1.0)
        if not onebranch.tonode==-1:
            fimrow.append(onebranch.branchid[0])
            fimcol.append(onebranch.tonode[0]+nnode)
            fimdata.append(-1.0)
        if not onebranch.frnode[1]==-1:
            fimrow.append(onebranch.branchid[0])
            fimcol.append(onebranch.frnode[1]+nnode)
            fimdata.append(-onebranch.ar)
        if not onebranch.tonode[1]==-1:
            fimrow.append(onebranch.branchid[0])
            fimcol.append(onebranch.tonode[1]+nnode)
            fimdata.append(onebranch.ar)
        
        frerow.append(onebranch.branchid[1])
        frecol.append(onebranch.branchid[1]+2*nnode)
        fredata.append(1.0)        
        frerow.append(onebranch.branchid[1])
        frecol.append(onebranch.branchid[0]+2*nnode)
        fredata.append(onebranch.ar)
        
        fimrow.append(onebranch.branchid[1])
        fimcol.append(onebranch.branchid[1]+2*nnode+n2branch)
        fimdata.append(1.0)        
        fimrow.append(onebranch.branchid[1])
        fimcol.append(onebranch.branchid[0]+2*nnode+n2branch)
        fimdata.append(onebranch.ar) 
    row = np.array(frerow)
    col = np.array(frecol)
    data = np.array(fredata)
    fre=csr_matrix((data, (row, col)), shape=(n2branch,2*n2branch+2*nnode))
    row = np.array(fimrow)
    col = np.array(fimcol)
    data = np.array(fimdata)
    fim=csr_matrix((data, (row, col)), shape=(n2branch,2*n2branch+2*nnode))
    
    J=scipy.sparse.vstack([Jup,fre,fim],format="csr")
    
    for iter in range(8):   
        for j in range(len(powsys.onephasepqbrancharray)):
            t=onephasepqbranch()
            t=powsys.onephasepqbrancharray[j]
            t.ire=np.real((t.p+1j*t.q)/(dx[t.frnode]+1j*dx[t.frnode+nnode]))
            t.iim=-np.imag((t.p+1j*t.q)/(dx[t.frnode]+1j*dx[t.frnode+nnode]))
            if iter==0:
                #print t.ire
                #print t.iim
                ival=t.ire+1j*t.iim
                sval=t.p+1j*t.q
                vval=dx[t.frnode]+1j*dx[t.frnode+nnode]
                #print vval
                #print t.frnode
                #print t.frnodename
                #print nodearray['4c']
                #print 'i',ival
                #print 'v',vval
                #print 's',sval
                #print 'i',np.abs(ival),'<',np.rad2deg(np.angle(ival))
                #print 's',np.abs(sval),'<',np.rad2deg(np.angle(sval))
                #print 'v',np.abs(vval),'<',np.rad2deg(np.angle(vval))
                #print vval
            rval[2*nnode+t.branchid]=t.ire
            rval[2*nnode+n2branch+t.branchid]=t.iim
        F=np.r_[rval]
        if iter==1:
            pass
            #print 'iter=1,v4a',dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
            #print 'iter=1,v3a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]
            #print 'iter=1,v34a',dx[nodearray['3a']]+1j*dx[nodearray['3a']+nnode]-(dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode])
            #print 'iter=1,v4b',dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
            #print 'iter=1,v4c',dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]
            #print 'i1a',(dx[2*nnode]+1j*dx[2*nnode+n2branch]) 
            #v4a=dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
            #print 'v4a',np.abs(v4a),np.angle(v4a)
            #print 'rval',F        
        dx=linalg.spsolve(J, F)

    v4a120=dx[nodearray['4a']]+1j*dx[nodearray['4a']+nnode]
    v4b120=dx[nodearray['4b']]+1j*dx[nodearray['4b']+nnode]
    v4c120=dx[nodearray['4c']]+1j*dx[nodearray['4c']+nnode]
    #print 'v4a120',np.abs(v4a120)/20.0,np.rad2deg(np.angle(v4a120))
    #print 'v4b120',np.abs(v4b120)/20.0,np.rad2deg(np.angle(v4b120))
    #print 'v4c120',np.abs(v4c120)/20.0,np.rad2deg(np.angle(v4c120))
    for nreg in range(len(powsys.onephaseregulatorarray)):
        reg=onephaseregulator()
        reg=powsys.onephaseregulatorarray[nreg]
        #print 'tap0',reg.tap0
        #print np.abs(tap[nreg]-reg.tap0)
        y[str(nreg)].append(float(tap[nreg]))
    xiter.append(nregiter)
print xiter
print y['0']
print y['1']
print y['2']
x=[0, 1, 2, 3, 4]
ya=[20.0, 20.0, 20.0, 20.0, 20.0]
yb=[0.0, 1.0, 2.0, -2.0, -2.0]
yc=[20.0, 18.0, 16.0, 17.0, 17.0]
    

#print v3
#vb34=v3-v4
#print vb34
#print dx
#np.linalg.inv(A)