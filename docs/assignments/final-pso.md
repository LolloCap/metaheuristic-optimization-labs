# Final project Particle Swarm Optimization

## Objective

Study Particle Swarm Optimization on the Rastrigin function and compare it with best-neighbor Local Search. Explain the balance between exploration, exploitation, robustness, and evaluation cost.

## PSO configuration

- 30 particles with random initial positions and zero initial velocities.
- Circular communication topology. Each particle communicates with four neighbors.
- Inertia `w = 0.7`, cognitive coefficient `c1 = 1.5`, and social coefficient `c2 = 1.5`.
- Two-dimensional domain `[-5.12, 5.12]^2`.
- 100 update cycles.
- An explicit strategy for positions that reach the search boundary.

## Local Search baseline

Begin at a random point. At each of 100 iterations, generate ten neighbors by independently perturbing every coordinate by a uniform value in `[-0.1, 0.1]`. Select the best improving neighbor.

## Expected analysis

Execute both methods five times. Report every result and objective-evaluation count, followed by mean and standard deviation. Compare the two algorithms using the same type of global table used in earlier practices. Two-dimensional or three-dimensional PSO trajectory visualization is optional.

The requested submission consists of executable source code and a report containing tables, design decisions, implementation difficulties, and analysis. The deadline in the brief is 23 June 2025.

## Source brief

This page summarizes the original Spanish course brief. The PDF is retained in the author's local archive and is not redistributed; see the [source-brief policy](../../assignments/es/README.md).
