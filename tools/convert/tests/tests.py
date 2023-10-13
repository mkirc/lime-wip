import pathlib

import h5py
import numpy as np

from flashBlock import FlashBlockFactory
from helper import setupLIMEStage1, centerAxis


def singleBlockTest():
    testDir = pathlib.Path(__file__).parent.absolute()
    plotFile0 = testDir.joinpath("SpitzerTest_hdf5_plt_cnt_0000")
    singleBlockOutFile = testDir.joinpath("single_block_stage_1.h5")

    with h5py.File(f"{str(singleBlockOutFile)}", "w") as outFile:
        flashFile = h5py.File(plotFile0, "r")

        ff = FlashBlockFactory(flashFile)

        block = next(ff.generateBlocksForSlice(slice(0, 1)))

        x1 = centerAxis(block.gridpoints[:, 0])

        radius = np.max(x1)  # assumes cubic block

        minscale = 2 * np.max(x1) / 8  # assumes cubic centered block with nxb=8

        lime_x1, lime_x2, lime_x3 = setupLIMEStage1(
            outFile, n_blocks=1, radius=radius, minscale=minscale
        )

        lime_x1[0:512] = x1
        lime_x2[0:512] = centerAxis(block.gridpoints[:, 1])
        lime_x3[0:512] = centerAxis(block.gridpoints[:, 2])
