# Implementation guide

The code is organized as a small Python package so that the objective functions and shared operators have one definition. The experiment scripts contain the course-specific run counts and parameter choices.

## Core modules

| Module | Responsibility |
| --- | --- |
| `qap.py` | QAPLIB parser, permutation validation, full objective, and O(n) swap evaluation |
| `results.py` | Common optimization result and convergence-history records |
| `neighborhood.py` | Greedy, Random Search, two local-search variants, Simulated Annealing, and Tabu Search |
| `multistart.py` | Randomized greedy construction, GRASP, ILS, and VNS |
| `evolutionary.py` | OX crossover, cyclic mutation, Simple GA, CHC, and clearing-based Multimodal GA |
| `pso.py` | Rastrigin, ring-topology PSO, continuous Local Search, and trajectory plots |

## Representation

A QAP solution is a zero-based permutation `p`. Facility `i` is assigned to location `p[i]`. The public methods validate that each candidate contains every integer from `0` through `n - 1` exactly once.

The full objective costs O(n²). A 2-opt neighbor is evaluated in O(n) with `QAPInstance.swap_cost`, which avoids recomputing terms unaffected by the swap. The tests compare this delta calculation with full evaluation over many permutations and every possible swap in a small instance.

## Reproducible randomness

Each stochastic function accepts `seed`. A local `numpy.random.Generator` owns the random state for that run, so experiments do not depend on process-global random state. The command-line experiments publish their seed sequence directly in code.

## Search safeguards

- Tabu Search always selects a valid move. If every sampled move is tabu and fails aspiration, it temporarily chooses the best sampled move instead of producing an invalid state.
- Restarted Tabu Search solutions are evaluated immediately, so the stored solution and objective remain synchronized.
- VNS uses a bounded loop and therefore performs exactly `max_local_searches` local-search calls.
- CHC keeps a constant population size, uses elitist parent-offspring survival, lowers its threshold only when no child enters the population, and records restart events.
- Multimodal GA applies clearing to selection fitness while retaining the complete population.
- PSO uses the assignment's 100-update default. When a coordinate crosses a bound, it is clipped and its velocity component is reset to zero.

## Experiment entry points

The four modules in `experiments/` expose the course sequence. QAP scripts accept `--data-dir`, repeatable `--dataset`, and `--quick`. The quick mode changes only computational budgets, making it suitable for smoke testing; the normal mode retains the assignment settings.

The final PSO entry point accepts `--iterations`, `--runs`, and an optional `--output-dir`. Its defaults run five independent 100-update experiments for both PSO and Local Search. When an output directory is supplied, it writes per-run and summary CSV files plus two trajectory figures.
