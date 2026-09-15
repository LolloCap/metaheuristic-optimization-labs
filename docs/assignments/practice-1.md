# Practice 1 Neighborhood and trajectory algorithms

## Objective

Implement Random Search, Local Search, Simulated Annealing, and Tabu Search for the Quadratic Assignment Problem. Compare their results with a deterministic Greedy construction on the `Tai25b`, `Sko90`, and `Tai150b` instances.

## Required methods

- Random Search generates an independent permutation at every iteration, runs for `1000 x n` iterations, and is repeated five times with different seeds.
- Local Search uses the swap or 2-opt neighborhood. Best Improvement examines every neighbor; the randomized First-Improvement variant changes the inspection order. Each variant is repeated five times.
- Simulated Annealing uses Cauchy cooling. At a temperature it stops after five accepted or forty generated neighbors. Initial temperature is calculated with `mu = phi = 0.3`; the run performs `50 x n` cooling steps and is repeated five times.
- Tabu Search examines forty neighbors per iteration, stores moves in a tabu list of initial size `n / 2`, and uses aspiration. It runs for `40 x n` iterations and restarts every `8 x n` iterations. Restart probabilities are 0.25 random, 0.50 greedy, and 0.25 best-known; tenure changes by 50 percent after a restart. It is repeated ten times.
- Greedy pairs high-flow facilities with low-total-distance locations.

## Expected analysis

For every instance and stochastic method, record objective value and the iteration or evaluation at which the best solution is found. Summarize best, mean, worst, and standard deviation, then compare solution quality, robustness, convergence behavior, and computational work.

## Source brief

This page summarizes the original Spanish course brief. The PDF is retained in the author's local archive and is not redistributed; see the [source-brief policy](../../assignments/es/README.md).
