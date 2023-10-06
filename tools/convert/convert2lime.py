import sys

import h5py
import numpy as np


if __name__ == "__main__":

    flash_file = h5py.File(sys.argv[1])

    all_nodes = np.array(flash_file["node type"])
    bb = flash_file["bounding box"]
    temp = flash_file["temp"]
    dens = flash_file["dens"]

    velx = flash_file["velx"]
    vely = flash_file["vely"]
    velz = flash_file["velz"]

    nxb = nyb = nzb = range(8)
    N = 10


    Ix, Iy, Iz = np.meshgrid(nxb, nyb, nzb, indexing='ij')

    leaves = np.where(all_nodes == 1)[0]



    points = np.empty((N,512,3))
    velocities = np.empty((N,512,3))

    temperatures = np.empty((N,512))
    densities = np.empty((N,512))

    def pointsForNode(node):
        (dx, x0), (dy, y0), (dz, z0) = [(bb[node][i][1]-bb[node][i][0],
                                         bb[node][i][0]) for i in range(3)]
        return np.array([Ix * dx + x0,
                         Iy * dy + y0,
                         Iz * dz + z0]).reshape(3,-1).T

    def velocitiesForNode(node):
        return np.array([velx[node].flatten(),
                         vely[node].flatten(),
                         velz[node].flatten()]).T

    for idx, leaf in enumerate(leaves[:N]):
        temperatures[idx] = temp[leaf].flatten()
        densities[idx] = dens[leaf].flatten()
        velocities[idx] = velocitiesForNode(leaf)
        p = pointsForNode(leaf)
        points[idx] = p

    points = points.reshape((N*512, 3))
    velocities = velocities.reshape((N*512, 3))

    temperatures = temperatures.reshape(N*512)
    densities = densities.reshape(N*512)


