import numpy as np
import os, sys


def LDOS_xw(omega, V, E, ee):
    N = int(np.sqrt(V.shape[0] / 2))
    u = V[:N**2, :]
    v = V[N**2:, :]

    L1 = ee / ((omega - E) ** 2 + ee ** 2) / np.pi
    L2 = ee / ((omega + E) ** 2 + ee ** 2) / np.pi

    u = np.abs(u) ** 2
    v = np.abs(v) ** 2

    A = u@L1 + v@L2

    A = np.reshape(A, (N, N))

    return A

if len(sys.argv) != 5:
    print("Usage: python BatchLDOS.py <N> <result root path> <output name> <ee>")
    exit(1)

N = int(sys.argv[1])
omega = 0
resDir = sys.argv[2]
outputFn = sys.argv[3]
ee = float(sys.argv[4])

subdirs = [x[0] for x in os.walk(resDir)][1:]

acc = np.zeros((N, N), dtype=np.float64)
for d in subdirs:
    print(f"Process folder {d}")
    Efiles = [f for f in os.listdir(d) if "E_" in f]
    Vfiles = [f for f in os.listdir(d) if "V_" in f]
    Efiles.sort()
    Vfiles.sort()
    for i in range(len(Efiles)):
        E = np.load(os.path.join(d, Efiles[i]))
        V = np.load(os.path.join(d, Vfiles[i]))
        acc += LDOS_xw(omega, V, E, ee)
        del E
        del V

np.save(outputFn, acc)
print("Finished.")