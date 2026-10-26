import numpy as np
K=[(0,0),(0.45,0.22),(1.55,0.67),(2.25,1.15),(2.32,1.22),(3.45,1.66),(3.62,1.80),(4.55,2.22),(4.99,2.5),
   (14.18,3.92),(15.3,4.47),(16.3,5.3),(17.4,6.05),(18.0,6.6),(18.3,7.0),(18.36,8.27),(18.6,8.5)]
C=[18.6,22.0,23.9,26.4,28.6,31.3,34.6]
for k in range(6):
    B,D,st=C[k],C[k+1]-C[k],8.5+k
    K+=[(B+0.4,st+0.4),(B+D-0.14,st+0.86),(B+D,st+1)] if k<5 else [(B+0.4,st+0.4),(B+D-0.22,st+0.78),(B+D,st+1)]
K+=[(37.7,16.62),(38.17,17.0),(39.0,17.72),(39.6,18.08),(40.3,18.4),(42.6,20.0)]
OUT=np.array([a for a,b in K]); SRC=np.array([b for a,b in K])
assert np.all(np.diff(OUT)>0) and np.all(np.diff(SRC)>0), K
DUR=42.6
def src(T): return float(np.interp(T,OUT,SRC))
def out(s): return float(np.interp(s,SRC,OUT))
