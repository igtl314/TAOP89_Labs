from operator import inv
import numpy as np
from numpy import dot
from numpy import transpose
from numpy.linalg import inv
import time
import sys

filc = " ".join(sys.argv[1:]).split('.')[0]+'.npz'
npzfile = np.load(filc)
c = npzfile['c']
b = npzfile['b']
A = npzfile['A']

bix = npzfile['bix']
zcheat = npzfile['zcheat']
xcheat = npzfile['xcheat']

bix = bix-1

t1 = time.time()

[m, n] = np.shape(A)
print('Rows: '+repr(m)+' cols: '+repr(n))

# Start iterations
iter = 0
 # Create nix

# We follow "Simplexmetoden i matrisform" from the book.
while iter >= 0:
    iter += 1

    #Step 1 (and 12)
    nix = np.setdiff1d(range(n), bix)
    B = A[:, bix]
    N = A[:, nix]
    cB = c[bix]
    cN = c[nix]
    #Step 2
    Binv = inv(B)
    #Step 3
    bhatt = dot(inv(B),b)
    #Step 4 - dualen
    y = transpose(dot(transpose(cB),Binv))
    #Step 5 - målfunktionsvärdet
    z=dot(transpose(b),y)

    # calc right-hand-sides and reduced costs
    # --------
    #Step 6 - reducerade kostnader
    cnhatt = cN - dot(transpose(N),y)

    # calc most negative reduced cost, rc_min,
    # and index for entering variable, inkvar
    # --------
    #Step 8 - inkommande variabel
    inix = np.argmin(cnhatt) #Hittar med största(mest negativa) reducerad kostnad
    rc_min = cnhatt[inix] 
    inkvar = nix[inix]

    #Step 7 - optimum?
    if rc_min >= -1.0E-12:
        print('Ready')
        iter = -1
        
        # construct solution, x, and check it
        x = np.zeros(n)
        for i in range (len(bix)):                
            x[bix[i]] = bhatt[i]
        
        diffx = np.linalg.norm(x-xcheat)
        diffz = z-zcheat
        print ('xdiff: '+repr(diffx))
        print ('zdiff: '+repr(diffz))
        # print('z: ',z)
    else:
        # calc entering column, a
        #Step 9
        ahatt = dot(Binv, A[:,inkvar])

        if max(ahatt) <= 0:
            # unbounded solution
            print('Unbounded solution!')
            iter = -1
        else:
            # calc leaving var, utgvar
            # --------
            # Step 11 - Finn minsta positiva kvot
            kvot = bhatt/ahatt
            utix = np.where(kvot > 0, kvot, np.inf).argmin() #Ersätt alla tal =<0 med +inf och hitta lägsta index
            utgvar = bix[utix]
            
            print(' Iter: '+repr(iter)+' z: '+repr(z)+' rc: ' + repr(rc_min)+' ink: '+repr(inkvar+1)+' utg: '+repr(utgvar+1))
         
            # make new partition
            # --------
            bix[utix] = nix[inix]


elapsed = time.time() - t1
print('Elapsed time: '+repr(elapsed))