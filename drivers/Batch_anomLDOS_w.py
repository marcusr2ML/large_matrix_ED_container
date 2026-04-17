import numpy as np
import os, sys


def anom_LDOS_w(V, E, ee):
    N = int(np.sqrt(V.shape[0] / 2))
    w = np.linspace(-.5, .5, 1001);


    pos_inds = E > 0
    E   = E[pos_inds]
    V 	= V[:, pos_inds]

    u = V[:N**2, :]
    v = V[N**2:, :]
    u = u.reshape((N, N, V.shape[1]))
    v = v.reshape((N, N, V.shape[1]))

    xv, yv = np.meshgrid(w, E)

    wp = xv + yv
    wm = xv - yv

    L2 = ee / (wp**2 + ee**2) / np.pi
    L1 = ee / (wm**2 + ee**2) / np.pi

    
    p = (np.multiply(u,np.conjugate(v)) @(L1- L2)).reshape((N, N, w.shape[0]))


    return p

if len(sys.argv) != 5:
    print("Usage: python BatchKw_fft.py <N> <result root path> <output name> <ee>")
    exit(1)

N = int(sys.argv[1])
omega = 0
resDir = sys.argv[2]
outputFn = sys.argv[3]
ee = float(sys.argv[4])

subdirs = [x[0] for x in os.walk(resDir)][1:]

pwAcc = np.zeros((N, N, 1001), dtype=np.complex128)
for d in subdirs:
    print(f"Process folder {d}")
    Efiles = [f for f in os.listdir(d) if "E_" in f]
    Vfiles = [f for f in os.listdir(d) if "V_" in f]
    Efiles.sort()
    Vfiles.sort()
    for i in range(len(Efiles)):
#        E = np.load(os.path.join(d, Efiles[i]))
#        V = np.load(os.path.join(d, Vfiles[i]))

        Vpath = os.path.join(d, Vfiles[i])
        Epath = os.path.join(d, Efiles[i])
        try:
            V = np.load(Vpath)
            print(f"Loaded V: {Vpath}, shape={V.shape}, size={V.size}")
            if V.shape[1] == 2 * N**2:
                V = V.T
        except Exception as e:
            print(f"Failed to load {Vpath}: {e}")
            continue
        try:
            E = np.load(Epath)
        except Exception as e:
            print(f"Failed to load {Epath}: {e}")
            continue


       
        Lp = anom_LDOS_w(V, E, ee)
       
        pwAcc += Lp
       

        del E
        del V

np.save("aL_" + outputFn, pwAcc)


print("Finished.")
