import numpy as np
import scipy.io
import os, sys
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: python BatchNpy2Mat.py <result root path> <output path>")
    exit(1)

resDir = sys.argv[1]
outDir = sys.argv[2]
subdirs = [x[0] for x in os.walk(resDir)][1:]

# Create output directory if not exist
Path(outDir).mkdir(exist_ok=True)

i = 0
for d in subdirs:
    print(f"Process folder {d}")
    Efiles = [f for f in os.listdir(d) if "E_" in f]
    Vfiles = [f for f in os.listdir(d) if "V_" in f]
    Efiles.sort()
    Vfiles.sort()


    for i in range(len(Efiles)):
        eigval = np.load(os.path.join(d, Efiles[i]))
        eigvec = np.load(os.path.join(d, Vfiles[i]))
        scipy.io.savemat(os.path.join(outDir, f"Eig-{i}.mat"), dict(E=eigval, V=eigvec), do_compression=True, oned_as='column')
        del eigval
        del eigvec
        i += 1

print("Finished.")