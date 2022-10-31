#TAOP89 Marcus Döberl (mardo435) York F.v Wangenheim (yorfr185)
#Tar emot filer och lägger till .mat, används med mat filer
import numpy as np
import time
import sys
import copy
import scipy.io

e=100
print("enter file name: ", end="")
fil = input()  
prob = fil
fil= fil +".mat"
print("Reading data from file '" + fil + "'")

if fil==None:
    print('File '+repr(fil)+' does n ot exist')
    exit()

print('Datafile: '+repr(fil))
mat=scipy.io.loadmat(fil,squeeze_me=True)

m=mat['m'] #antal möjliga locations för en fabrik
n=mat['n'] #antalet kunder 
s=mat['s'] #kapaciteten hos en fabrik på plats i    
d=mat['d'] #efterfrågan hos en kund j
f=mat['f'] #fasta kostnade för en anläggning på plats i
c=mat['c'] #transportkostnaden per enhet till kund j från anläggning i
print ('m:',m,' n:',n)
print ('s:',s)
print ('d:',d)
print ('f:',f)
print ('c:',c)

t1=time.time()
x=np.zeros((m,n),dtype=np.int)
y=np.zeros((m),dtype=np.int)

ss=copy.deepcopy(s)
dd=copy.deepcopy(d)
print('ss', ss)
print('dd', dd)



while sum(dd)>0:
    for kund in range(0,n): # Går igenom varje kund 
        while(dd[kund]>0): #och stannar på kunden så länge den har en efterfrågan kvar
            fabrik = np.where(c[:,kund] == np.amin(c[:,kund]))[0][0] #Hittar den fabrik med billigast transportkostand till angiven kund
            y[fabrik] = 1 #Sätter att vi använder kunden
            if(ss[fabrik] > dd[kund]): #Om fabriken kan ta hand om hela kundens efterfrågan
                ss[fabrik] -= dd[kund]
                x[fabrik,kund] = dd[kund]
                dd[kund] = 0
            elif(ss[fabrik] <= dd[kund]): # Om fabriken inte kan det, använd den så mycket som möjligt
                dd[kund] -= ss[fabrik]
                x[fabrik,kund] = ss[fabrik]
                ss[fabrik] = 0 #Fabrikens kapacitet är nu slut
                c[fabrik,:] = 2147483647 #Sätter alla transportkostnander från den tomma fabriken till oöndligheten
            
        if(sum(dd)<= 0):
            break
                

    print('Efterfrågan kvar',sum(dd))

    # set x and yli
    # deduct from ss and dd, 
    # --------
    
elapsed = time.time() - t1
print ('Tid: '+str('%.4f' % elapsed + "s"))

cost=sum(sum(np.multiply(c,x))) + e*np.dot(f,y)
print ('Problem:',prob,' Totalkostnad: '+str(cost))
print ('y:',y)
print ('Antal byggda fabriker:',sum(y),'(av',m,')')