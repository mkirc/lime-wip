import sys
import h5py

import numpy as np

from helper import euclidianValue


class FlashBlockFactory:
    def __init__(self, flash_file):
        self.file = flash_file
        self.bb = self.file["bounding box"]
        self.temperatures = self.file["temp"]
        self.dusttemperatures = self.file["tdus"]
        self.vels = (self.file["velx"], self.file["vely"], self.file["velz"])
        self.mags = (self.file["magx"], self.file["magy"], self.file["magz"])
        self.densities = self.file["dens"]
        self.blocks = np.array(self.file["node type"])
        self.leaves = np.where(self.blocks == 1)[0]  # node type == 1 -> leaf

    def velocitiesForBlock(self, blockId):
        return (self.vels[0][blockId], self.vels[1][blockId], self.vels[2][blockId])

    def magfluxesForBlock(self, blockId):
        return (self.mags[0][blockId], self.mags[1][blockId], self.mags[2][blockId])

    def generateBlocksForSlice(self, blockslice):
        for blockId in self.leaves[blockslice]:
            yield self.createBlock(blockId)

    def createBlock(self, blockId):
        return FlashBlock(
            blockId,
            self.bb[blockId],
            self.temperatures[blockId],
            self.dusttemperatures[blockId],
            self.densities[blockId],
            self.velocitiesForBlock(blockId),
            self.magfluxesForBlock(blockId),
        )


class FlashBlock:
    def __init__(self, blockId, bb, temp, tempdust, dens, vels, mags):
        self.id = blockId
        self.nxb, self.nyb, self.nzb = dens.shape
        self._Ix, self._Iy, self._Iz = np.meshgrid(
            range(self.nxb), range(self.nyb), range(self.nzb), indexing="ij"
        )

        self.gridpoints = self.gridpointsForBoundingbox(bb)
        self.temperatures = self.temperatures(temp)
        self.dusttemperatures = self.dusttemperatures(tempdust)
        self.densities = self.densities(dens)
        self.velocities = self.velocities(vels)
        self.magfluxes = self.magfluxes(mags)

    def gridpointsForBoundingbox(self, bb):
        (dx, x0), (dy, y0), (dz, z0) = [
            (bb[i][1] - bb[i][0], bb[i][0]) for i in range(3)
        ]
        return (
            np.array([self._Ix * dx + x0, self._Iy * dy + y0, self._Iz * dz + z0])
            .reshape(3, -1)
            .T
        )

    def velocities(self, velocities):
        return euclidianValue(velocities)

    def magfluxes(self, magfluxes):
        return euclidianValue(magfluxes)

    def densities(self, densities):
        return densities.flatten()

    def temperatures(self, temperatures):
        return temperatures.flatten()

    def dusttemperatures(self, dusttemperatures):
        return dusttemperatures.flatten()
