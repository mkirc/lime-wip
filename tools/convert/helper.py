import numpy as np
import h5py
from h5py import string_dtype
from h5py import Datatype
from h5py.h5t import TypeID, STR_NULLTERM

def center_axis(arraylike):
    return arraylike - (np.min(arraylike) - np.max(arraylike))


def euclidianValue(euclidian):
    return np.array(
        [euclidian[0].flatten(), euclidian[1].flatten(), euclidian[2].flatten()]
    ).T


def nulltermStringType(length):
    type_id = TypeID.copy(h5py.h5t.C_S1)
    type_id.set_size(length)
    type_id.set_strpad(STR_NULLTERM)
    return h5py.Datatype(type_id)


def setup_lime_stage_one(outFile, n_blocks, radius=0., minscale=0.):
    outFile.attrs.create("RADIUS  ", radius, dtype=np.float64)
    outFile.attrs.create("MINSCALE", minscale, dtype=np.float64)
    outFile.attrs.create("NSOLITER", 0, dtype=np.int32)
    grid_grp = outFile.create_group("GRID")
    grid_grp.attrs.create("CLASS", "HDU", dtype=nulltermStringType(4))
    grid_grp.attrs.create("COLLPAR1", "H2", dtype=nulltermStringType(3))
    grid_grp.attrs.create("EXTNAME", "GRID", dtype=nulltermStringType(5))
    grid_grp.attrs.create("HDUNUM", 0, dtype=np.int32)
    cols_grp = outFile.create_group("GRID/columns")
    cols_grp.attrs.create("CLASS", "DATA_GROUP", dtype=nulltermStringType(11))
    lime_id = outFile.create_dataset(
        "GRID/columns/ID",
        (n_blocks * 512),
        dtype=np.uint32,
        data=np.arange(n_blocks * 512),
    )
    lime_id.attrs.create("CLASS", "COLUMN", dtype=nulltermStringType(7))
    lime_id.attrs.create("COL_NAME", "ID", dtype=nulltermStringType(3))
    lime_id.attrs.create("POSITION", 1, dtype=np.int32)
    lime_id.attrs.create("UNIT", "", dtype=nulltermStringType(1))
    lime_is_sink = outFile.create_dataset(
        "GRID/columns/IS_SINK", (n_blocks * 512), dtype=np.int16
    )
    lime_is_sink.attrs.create("CLASS", "COLUMN", dtype=nulltermStringType(7))
    lime_is_sink.attrs.create("COL_NAME", "IS_SINK", dtype=nulltermStringType(8))
    lime_is_sink.attrs.create("POSITION", 5, dtype=np.int32)
    lime_is_sink.attrs.create("UNIT", "", dtype=nulltermStringType(1))

    lime_x1 = outFile.create_dataset(
        "GRID/columns/X1", (n_blocks * 512), dtype=np.float64
    )
    lime_x1.attrs.create("CLASS", "COLUMN", dtype=nulltermStringType(7))
    lime_x1.attrs.create("COL_NAME", "X1", dtype=nulltermStringType(3))
    lime_x1.attrs.create("POSITION", 2, dtype=np.int32)
    lime_x1.attrs.create("UNIT", "m", dtype=nulltermStringType(2))

    lime_x2 = outFile.create_dataset(
        "GRID/columns/X2", (n_blocks * 512), dtype=np.float64
    )
    lime_x2.attrs.create("CLASS", "COLUMN", dtype=nulltermStringType(7))
    lime_x2.attrs.create("COL_NAME", "X2", dtype=nulltermStringType(3))
    lime_x2.attrs.create("POSITION", 3, dtype=np.int32)
    lime_x2.attrs.create("UNIT", "m", dtype=nulltermStringType(2))

    lime_x3 = outFile.create_dataset(
        "GRID/columns/X3", (n_blocks * 512), dtype=np.float64
    )
    lime_x3.attrs.create("CLASS", "COLUMN", dtype=nulltermStringType(7))
    lime_x3.attrs.create("COL_NAME", "X3", dtype=nulltermStringType(3))
    lime_x3.attrs.create("POSITION", 4, dtype=np.int32)
    lime_x3.attrs.create("UNIT", "m", dtype=nulltermStringType(2))

    return lime_x1, lime_x2, lime_x3
