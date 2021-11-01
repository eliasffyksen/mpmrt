from ryu.lib.mrtlib import MrtRecord
import mpmrt

def handler(record: MrtRecord) -> int:
    return record.to_jsondict()

r = mpmrt.Reader[dict](handler, True)

(reader, count) = r.read('./examples/latest-bview', workers=16)

print('Found %d records' % count)

count = 0
for record in reader:
    print('\r%d' % count, end='')
    count += 1
print()

print('done')
