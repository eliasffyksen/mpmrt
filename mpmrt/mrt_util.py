from io import FileIO
from typing import Iterable, Iterator, List
from ryu.lib import mrtlib as mrt

def mrt_read(f):
    for record in mrt.Reader(f):
        yield record

def get_as_paths(record):
    result = []
    for path_attr in record['bgp_message']['path_attributes']:
        if path_attr['type'] == [2, 'AS_PATH']:
            for as_path in path_attr['value']:
                if as_path['type'] != [2, 'AS_SEQUENCE']:
                    raise ValueError('Unknown AS_PATH type %s' % as_path['type'])
                result.append(as_path['value'])
    if len(result) == 0:
        raise ValueError('No AS_PATHS')
    return result

def mrt_indices(mrt_file: FileIO) -> List[int]:
    mrt_file.seek(0, 2)
    mrt_size = mrt_file.tell()
    mrt_file.seek(0)
    pos_new = 0
    result = []
    while pos_new < mrt_size:
        result.append(pos_new)
        mrt_file.seek(8, 1) # Seek to length
        mrt_msg_size = mrt_file.read(4) # Read length
        mrt_msg_size = int.from_bytes(mrt_msg_size, 'big')
        mrt_file.seek(mrt_msg_size, 1) # Seek to begining of next file
        pos_new = mrt_file.tell()
    return result
