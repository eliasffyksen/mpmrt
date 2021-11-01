from mpmrt import Reader

class Test:
    pass

def test_Reader():
    reader = Reader[Test]('./mrtfile')
    assert isinstance(reader, Reader)

test_Reader()