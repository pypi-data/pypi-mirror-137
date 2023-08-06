""" Test multithreading to ensure consistent behavior with serial implementation."""
import unittest
import warnings
from os import remove
from os.path import exists, join
import numpy as np
from AIMSim.chemical_datastructures import MoleculeSet
from time import time
import cProfile

from tabulate import tabulate

file = open(join("tests", "data", "combinatorial_1.txt"), "r")
data = file.readlines()
_500_molecules = data[1:1002]


_500_molecules_fpath = "temp_multithread_speedup_500.txt"
print(f"Creating text file {_500_molecules_fpath}", flush=True)
with open(_500_molecules_fpath, "w") as file:
    for smiles in _500_molecules:
        file.write(smiles)
print("Running 500 molecules with 1 process.", flush=True)
_500_molecules_serial_time = 0
start = time()
cProfile.run(
"""MoleculeSet(
    molecule_database_src=_500_molecules_fpath,
    molecule_database_src_type="text",
    is_verbose=False,
    similarity_measure="tanimoto",
    n_threads=1,
    fingerprint_type="morgan_fingerprint",
)""", filename="output.pstats", sort=-1)
_500_molecules_serial_time = time() - start

print("runtime:",_500_molecules_serial_time)



    # ... do something ...




