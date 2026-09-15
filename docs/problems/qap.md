# Quadratic Assignment Problem

## Problem statement

The Quadratic Assignment Problem assigns `n` facilities to `n` locations. Each pair of facilities has a flow, and each pair of locations has a distance. The objective is to place facilities so that large flows tend to travel over short distances.

For a permutation `p`, where facility `i` is assigned to location `p(i)`, this project minimizes:

```math
\min_{p \in S_n} f(p) = \sum_{i=1}^{n}\sum_{j=1}^{n} a_{ij} b_{p(i),p(j)}
```

`A = (a_ij)` is the flow matrix, `B = (b_kl)` is the distance matrix, and `S_n` is the set of all permutations of `n` locations. The product makes the objective quadratic: changing one assignment affects its interaction with every other assignment.

## Small example

Suppose facilities A and B exchange a large amount of material. Assigning them to nearby locations reduces the `flow x distance` term associated with that pair. The difficulty is that each location can hold only one facility, so improving one pair can make several other pairs worse.

The search space has `n!` solutions. This reaches approximately `1.55 x 10^25` assignments at `n = 25`, before the larger `n = 90` and `n = 150` instances are considered. Exhaustive enumeration is therefore impractical.

## QAPLIB file format

[QAPLIB](https://qaplib.mgi.polymtl.ca/) stores an instance as:

```text
n
A: n x n matrix
B: n x n matrix
```

The Python reader consumes whitespace-separated integers, validates the exact number of entries, and stores solutions as zero-based permutations. QAPLIB solution files contain the size, a published objective value, and a one-based permutation.

## Datasets

| Instance | Size | Family and structure | Course reference value | QAPLIB status |
| --- | ---: | --- | ---: | --- |
| `Tai25b` | 25 | Taillard `b` instance; asymmetric and randomly generated | 344,355,646 | Proven optimum |
| `Sko90` | 90 | Rectangular distances and pseudorandom flows | 115,534 | Best published feasible value; lower bound 112,423 |
| `Tai150b` | 150 | Taillard `b` instance; asymmetric and randomly generated | 498,896,643 | Best published feasible value; lower bound 441,786,736 |

The course brief calls the three numbers optimal reference costs. QAPLIB makes a finer distinction: `Tai25b` is proven optimal, while the listed `Sko90` and `Tai150b` values are best-known feasible solutions with nonzero gaps to published lower bounds. This distinction matters when interpreting relative error.

## Why these instances are useful

- `Tai25b` is small enough for rapid experimentation and has a certified optimum.
- `Sko90` tests how the methods scale to a substantially larger structured instance.
- `Tai150b` stresses evaluation efficiency and makes full neighborhood exploration expensive.
- Using the same three instances across Practices 1, 2a, and 2b makes algorithm families directly comparable.

## Evaluation and metrics

The experiments record objective cost and number of objective evaluations. Repeated stochastic runs also report best, mean, worst, and population standard deviation. Practice 2a additionally considers:

```math
RE = \frac{\bar{f} - f_{best}}{f_{best}} \times 100
```

```math
CV = \frac{\sigma}{\bar{f}} \times 100
```

`RE` describes how far the mean run lies above the best observed run. `CV` normalizes variability by the mean and is used as a robustness indicator.

## Data access

Run `python scripts/fetch_qaplib.py --with-solutions` from the repository root. The files are downloaded into `data/qaplib/` and are not committed. See [the data instructions](../../data/README.md).

## Source

The format, instance descriptions, feasible values, bounds, and solution classifications come from the [QAPLIB Problem Instances and Solutions page](https://qaplib.mgi.polymtl.ca/).
