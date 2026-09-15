# Rastrigin optimization problem

## Problem statement

The final project minimizes the standard Rastrigin function:

```math
f(x) = 10d + \sum_{i=1}^{d}\left(x_i^2 - 10\cos(2\pi x_i)\right)
```

The assignment uses `d = 2` and bounds each coordinate to `[-5.12, 5.12]`. The global minimum is:

```math
x^* = (0, 0), \qquad f(x^*) = 0
```

## Why it is difficult

The quadratic term creates a broad bowl centered at the origin. The cosine term overlays many regularly spaced local minima. A method that only makes small local moves can settle in one of these basins even when the global minimum is still far away.

Unlike QAP, Rastrigin is continuous: a candidate is a real-valued vector rather than a permutation. There is no external dataset file. The benchmark is completely defined by the function, dimension, bounds, and optimizer parameters.

## Experimental configuration

| Setting | PSO | Local Search baseline |
| --- | ---: | ---: |
| Dimensions | 2 | 2 |
| Domain | `[-5.12, 5.12]^2` | `[-5.12, 5.12]^2` |
| Population or neighbors | 30 particles | 10 neighbors per iteration |
| Updates | 100 | 100 |
| Independent runs | 5 | 5 |
| Objective evaluations | 3,030 per run | 1,001 per run |

The PSO uses inertia `w = 0.7`, cognitive coefficient `c1 = 1.5`, and social coefficient `c2 = 1.5`. Particles communicate through a ring: each particle considers the two nearest particles on either side. Boundary violations are clipped and the corresponding velocity components are set to zero.

The Local Search baseline begins at a random point. At every iteration it samples ten candidates by adding an independent uniform perturbation in `[-0.1, 0.1]` to each coordinate, clips candidates to the domain, and accepts the best improving neighbor.

## What the comparison measures

The experiment compares final objective value, evaluation cost, and variation across five seeded runs. The trajectory plots add a qualitative view: early particle motion shows exploration, while the later concentration of paths shows exploitation around a promising basin.

The formula, standard domain, multimodality, and global minimum are also described in this [open-access benchmark discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC4538776/#sec3-2).
