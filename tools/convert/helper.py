import numpy as np
import h5py
from h5py import string_dtype

def euclidianValue(euclidian):
    return np.array(
        [euclidian[0].flatten(), euclidian[1].flatten(), euclidian[2].flatten()]
    ).T


def setup_lime_file(outFile, n_blocks):
    outFile.attrs.create("RADIUS", 123.0, dtype=np.float64)
    grid_grp = outFile.create_group("GRID") 
    # label_arr =np.frombuffer('HDU'.encode("ascii"), dtype="|S1")
    type_id = h5py.h5t.TypeID.copy(h5py.h5t.C_S1)
    type_id.set_size(4)
    type_id.set_strpad(h5py.h5t.STR_NULLTERM)
    grid_grp.attrs.create("CLASS", "HDU", dtype=h5py.Datatype(type_id))
    grid_grp.attrs.create("COLLPAR1", "H2", dtype=string_dtype("ascii", 3))
    grid_grp.attrs.create("EXTNAME", "GRID", dtype=string_dtype("ascii", 5))
    grid_grp.attrs.create("HDUNUM", 0, dtype=np.int32)
    cols_grp = outFile.create_group("GRID/columns")
    cols_grp.attrs.create("CLASS", "DATA_GROUP", dtype=string_dtype("ascii", 11))
    lime_id = outFile.create_dataset(
        "GRID/columns/ID",
        (n_blocks * 512),
        dtype=np.uint32,
        data=np.arange(n_blocks * 512),
    )
    lime_id.attrs.create("CLASS", "COLUMN", dtype=string_dtype("ascii", 7))
    lime_id.attrs.create("COL_NAME", "ID", dtype=string_dtype("ascii", 3))
    lime_id.attrs.create("POSITION", 1, dtype=np.int32)
    lime_id.attrs.create("UNIT", "", dtype=string_dtype("ascii", 1))
    lime_is_sink = outFile.create_dataset(
        "GRID/columns/IS_SINK", (n_blocks * 512), dtype=np.int16
    )
    lime_is_sink.attrs.create("CLASS", "COLUMN", dtype=string_dtype("ascii", 7))
    lime_is_sink.attrs.create("COL_NAME", "IS_SINK", dtype=string_dtype("ascii", 8))
    lime_is_sink.attrs.create("POSITION", 5, dtype=np.int32)
    lime_is_sink.attrs.create("UNIT", "", dtype=string_dtype("ascii", 1))

    lime_x1 = outFile.create_dataset(
        "GRID/columns/X1", (n_blocks * 512), dtype=np.float64
    )
    lime_x1.attrs.create("CLASS", "COLUMN", dtype=string_dtype("ascii", 7))
    lime_x1.attrs.create("COL_NAME", "X1", dtype=string_dtype("ascii", 3))
    lime_x1.attrs.create("POSITION", 2, dtype=np.int32)
    lime_x1.attrs.create("UNIT", "m", dtype=string_dtype("ascii", 2))

    lime_x2 = outFile.create_dataset(
        "GRID/columns/X2", (n_blocks * 512), dtype=np.float64
    )
    lime_x2.attrs.create("CLASS", "COLUMN", dtype=string_dtype("ascii", 7))
    lime_x2.attrs.create("COL_NAME", "X2", dtype=string_dtype("ascii", 3))
    lime_x2.attrs.create("POSITION", 3, dtype=np.int32)
    lime_x2.attrs.create("UNIT", "m", dtype=string_dtype("ascii", 2))

    lime_x3 = outFile.create_dataset(
        "GRID/columns/X3", (n_blocks * 512), dtype=np.float64
    )
    lime_x3.attrs.create("CLASS", "COLUMN", dtype=string_dtype("ascii", 7))
    lime_x3.attrs.create("COL_NAME", "X3", dtype=string_dtype("ascii", 3))
    lime_x3.attrs.create("POSITION", 4, dtype=np.int32)
    lime_x3.attrs.create("UNIT", "m", dtype=string_dtype("ascii", 2))

    return lime_x1, lime_x2, lime_x3
