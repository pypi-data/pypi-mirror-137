import cppyy
import ctypes
import numpy as np

from quickstats.interface import cppyy as interface_cppyy

ctype_maps = {
    np.dtype('bool'): ctypes.c_bool,
    np.dtype('byte'): ctypes.c_byte,
    np.dtype('ubyte'): ctypes.c_ubyte,
    np.dtype('short'): ctypes.c_short,
    np.dtype('ushort'): ctypes.c_ushort,
    np.dtype('intc'): ctypes.c_int,
    np.dtype('uintc'): ctypes.c_uint,
    np.dtype('single'): ctypes.c_float,
    np.dtype('float32'): ctypes.c_float,
    np.dtype('double'): ctypes.c_double,
    np.dtype('float64'): ctypes.c_double,
    np.dtype('int64'): ctypes.c_int64,
    np.dtype('int32'): ctypes.c_int32
}

ctype_str_maps = {
    ctypes.c_int : "int",
    ctypes.c_uint : "unsigned int",
    ctypes.c_float : "float",
    ctypes.c_double : "double",
    ctypes.c_bool : "bool",
    ctypes.c_byte : "byte",
    ctypes.c_ubyte : "unsigned char",
    ctypes.c_short : "short",
    ctypes.c_ushort : "unsigned short",
    ctypes.c_int64 : "long",
    ctypes.c_long : "long",
}

np_type_str_maps = {
    np.dtype('bool'): "bool",
    np.dtype('byte'): "char",
    np.dtype('ubyte'): "unsigned char",
    np.dtype('short'): "short",
    np.dtype('ushort'): "unsigned short",
    np.dtype('intc'): "int",
    np.dtype('uintc'): "unsigned int",
    np.dtype('single'): "float",
    np.dtype('float32'): "float",
    np.dtype('double'): "double",
    np.dtype('float64'): "double",
    np.dtype('int64'): "long",
    np.dtype('int32'): "int"
}

def as_vector(data:np.ndarray):
    if data.ndim != 1:
        raise ValueError("data must be 1D array")
    c_type = ctype_maps.get(data.dtype, None)
    if c_type is None:
        raise ValueError(f"unsupported data type \"{data.dtype}\"")
    c_type_p = ctypes.POINTER(c_type)
    c_type_str = ctype_str_maps[c_type]
    c_data = data.ctypes.data_as(c_type_p)
    size = data.shape[0]
    result = cppyy.gbl.VecUtils.as_vector[c_type_str](c_data, size)
    return result

def as_c_array(data:np.ndarray):
    if data.ndim != 1:
        raise ValueError("data must be 1D array")
    c_type = ctype_maps.get(data.dtype, None)
    if c_type is None:
        raise ValueError(f"unsupported data type \"{data.dtype}\"")
    c_type_p = ctypes.POINTER(c_type)
    c_type_str = ctype_str_maps[c_type]
    c_data = data.ctypes.data_as(c_type_p)
    return c_data

def as_np_array(vec:cppyy.gbl.std.vector):
    if vec.value_type == 'std::string':
        return np.array([str(v) for v in vec])
    return np.array(vec.data())