# Practice 2a Multi-start search

## Objective

Implement GRASP, Iterated Local Search, and Variable Neighborhood Search for the same QAP instances used in Practice 1. Compare them with Greedy and First-Improvement Local Search. Use the optimized O(n) swap evaluation.

## Required methods

- GRASP constructs five randomized greedy solutions. At each construction step it samples from restricted candidate lists of size `l = 0.1 x n`, then applies First-Improvement Local Search. One complete GRASP run is reported per instance.
- ILS begins with a random permutation and Local Search. It performs nine further cycles in which the best solution is perturbed by randomly reordering a cyclic sublist of size `n / 4` and locally improved. Best-so-far acceptance is used, for ten Local Search calls in total.
- VNS starts with neighborhood index `k = 1`. It shakes the current solution with cyclic-sublist sizes `n/8`, `n/7`, `n/6`, `n/5`, and `n/4`, applies Local Search, resets `k` after improvement, and otherwise advances it. A run performs ten Local Search calls. Five runs are reported per instance.

## Expected analysis

Report objective cost and number of evaluations. Build per-run and global tables containing best, mean, worst, and standard deviation where applicable. Analyze convergence curves, VNS relative error, coefficient of variation, and evaluation growth with instance size.

## Source brief

This page summarizes the original Spanish course brief. The PDF is retained in the author's local archive and is not redistributed; see the [source-brief policy](../../assignments/es/README.md).
