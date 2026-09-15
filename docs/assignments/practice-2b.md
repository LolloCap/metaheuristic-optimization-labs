# Practice 2b Evolutionary algorithms

## Objective

Implement and compare a Simple Genetic Algorithm, CHC, and a Multimodal Genetic Algorithm on the three QAP instances. Use Greedy as a reference and execute every evolutionary algorithm five times per instance with the assigned seeds.

## Required methods

- The Simple GA may be stationary or generational. Choose a population between 30 and 200, use OX crossover with probability 0.90, tournament selection with `k = 10 percent of the population`, and cyclic opt-N mutation. The mutation study varies the affected fraction between 2 and 10 percent on `Sko90`.
- CHC uses the same population size as the Simple GA. Parents may cross only when their Hamming distance exceeds a threshold initialized to `L / 4`. CHC uses no ordinary mutation. If no child enters the population, decrease the threshold; at zero, retain the best chromosome and randomize the rest of the population. Plot convergence and identify restarts.
- The Multimodal GA extends the Simple GA with either sequential niching or clearing. The course implementation uses clearing based on Hamming distance.

## Expected analysis

For all five runs of each algorithm and instance, report cost and objective evaluations. Compare efficiency, solution quality, best individual result, mean result, robustness, and convergence. Show representative initial-versus-final population behavior.

## Source brief

This page summarizes the original Spanish course brief. The PDF is retained in the author's local archive and is not redistributed; see the [source-brief policy](../../assignments/es/README.md).
