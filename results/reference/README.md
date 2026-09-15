# Reproducible reference results

This directory contains deterministic results generated with the package entry points and the published seed sequence. The final PSO comparison uses seeds 0 through 4, 100 PSO updates, and 100 Local Search iterations.

Regenerate it from the repository root:

```bash
python -m experiments.final_pso --iterations 100 --runs 5 --output-dir results/reference/final-pso
```
