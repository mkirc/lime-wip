import sys

import h5py
import numpy as np

from flashBlock import FlashBlockFactory
from helper import setup_lime_file


if __name__ == "__main__":
    N_BLOCKS = 3

    with h5py.File(f"{sys.argv[2]}", "a") as outFile:
        lime_x1, lime_x2, lime_x3 = setup_lime_file(outFile, N_BLOCKS)

        flashFile = h5py.File(sys.argv[1], "r")

        ff = FlashBlockFactory(flashFile)

        i = 0
        for block in ff.generateBlocksForSlice(slice(0, N_BLOCKS)):
            lime_x1[i * 512 : (i + 1) * 512] = block.gridpoints[:, 0]
            lime_x2[i * 512 : (i + 1) * 512] = block.gridpoints[:, 1]
            lime_x3[i * 512 : (i + 1) * 512] = block.gridpoints[:, 2]
            i += 1
            del block

