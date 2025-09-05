import pathlib
import re
import sys

gen_py_dir = pathlib.Path(sys.argv[1])

# Process all *_pb2_grpc.py files
for f in gen_py_dir.glob("*_pb2_grpc.py"):
    text = f.read_text()

    # Replace top-level import of any *_pb2 module with relative import
    text = re.sub(r'^import (\S+_pb2)', r'from . import \1', text, flags=re.MULTILINE)

    f.write_text(text)