# QAPLIB datasets

Practices 1, 2a, and 2b use three instances from [QAPLIB](https://qaplib.mgi.polymtl.ca/):

| File | Size | Reference value used in the course |
| --- | ---: | ---: |
| `tai25b.dat` | 25 | 344,355,646 |
| `sko90.dat` | 90 | 115,534 |
| `tai150b.dat` | 150 | 498,896,643 |

Download the instances and their published solutions from the original host:

```bash
python scripts/fetch_qaplib.py --with-solutions
```

The files are placed in `data/qaplib/`. This directory is excluded from Git except for its placeholder, so benchmark files remain associated with their original source and terms. QAPLIB does not display a conventional software license for the instance collection on its main page; check the source site before redistributing the files.

The experiments can also use a manually prepared directory:

```bash
python -m experiments.practice_1 --data-dir path/to/qaplib
```

For the data format, objective function, instance families, and interpretation of the published reference values, see [the QAP guide](../docs/problems/qap.md).
