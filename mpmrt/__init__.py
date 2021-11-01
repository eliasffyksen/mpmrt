
from io import FileIO
from multiprocessing import Process, Queue
from ryu.lib import mrtlib as mrt
from typing import Any, TypeVar, Generic, Callable
from collections.abc import Iterator
from mpmrt.mrt_util import *

def _processor(queue: Queue, path: str, q_out: Queue, handler: Callable[[mrt.MrtRecord], Any]):
    mrt_file = open(path, 'rb')
    reader = mrt_read(mrt_file)
    while True:
        batch = queue.get()
        if batch == 'KYS':
            break
        mrt_file.seek(batch[0])
        out = []
        for _ in batch:
            res = handler(next(reader))
            if q_out != None:
                out.append(res)
        if q_out != None:
            q_out.put(out)
        del out
    mrt_file.close()   

def _read_iter(q_out: Queue, q_len):
    for _ in range(q_len):
        batch = q_out.get()
        for record in batch:
            yield record

T = TypeVar('T')

class Reader(Generic[T]):
    def __init__(
        self,
        handler: Callable[[mrt.MrtRecord], T],
        handler_result: bool=True
    ):
        self.handler = handler
        self.handler_result = handler_result
    
    
    def read(
        self,
        path: str,
        workers: int,
        batch_size: int=1000
    ) -> Iterator[T]:
        mrt_file = open(path, 'rb')
        indices = mrt_indices(mrt_file)

        queue = Queue((len(indices) // batch_size + 1) + workers)
        q_out = None
        if self.handler_result:
            q_out = Queue(len(indices) // batch_size + 1)

        batch = []
        count = 0
        for pos_new in indices:
            batch.append(pos_new)
            count += 1
            if len(batch) == batch_size:
                queue.put(batch)
                batch = []
        if len(batch):
            queue.put(batch)

        queue_len = queue.qsize()
        for _ in range(workers):
            queue.put('KYS')
        mrt_file.close()
        procs = []
        for i in range(workers):
            procs.append(Process(target=_processor, args=(queue, path, q_out, self.handler)))

        for proc in procs:
            proc.start()

        if q_out == None:
            return count
        return (_read_iter(q_out, queue_len), count)
