# Experimental results

These tables summarize the measurements produced for the course reports. QAP costs are minimized. The reference row contains the values supplied in the assignment; see the [QAP dataset notes](problems/qap.md) for the distinction between certified optima and best-known feasible solutions.

## Practice 1

| Algorithm | Tai25b best | Tai25b mean | Sko90 best | Sko90 mean | Tai150b best | Tai150b mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Reference | 344,355,646 | - | 115,534 | - | 498,896,643 | - |
| Greedy | - | 913,427,707 | - | 135,414 | - | 653,452,955 |
| Random Search | - | 464,606,461 | - | 131,484 | - | 617,992,374 |
| Best Improvement | 385,726,545 | 407,676,305 | 116,540 | 117,217 | 510,343,305 | 514,521,743 |
| First Improvement | 370,889,801 | 399,914,564 | 117,504 | 117,944 | 512,533,036 | 515,032,279 |
| Simulated Annealing | 344,594,778 | 352,869,871 | 115,846 | 116,120 | 506,397,569 | 507,807,455 |
| Tabu Search | 344,956,710 | 352,336,344 | 117,876 | 118,213 | 508,292,470 | 513,104,863 |

Simulated Annealing produced the strongest overall solution quality in these runs. On `Tai25b`, its best result is only about 0.069 percent above the certified optimum. Tabu Search was also competitive, while the two simple baselines remained far from the reference values. The Local Search variants reached useful solutions but required many swap evaluations.

## Practice 2a

GRASP and ILS each contain several internal starts and therefore have one reported aggregate per instance. VNS was run five times.

| Algorithm | Tai25b best | Tai25b mean | Sko90 best | Sko90 mean | Tai150b best | Tai150b mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GRASP | - | 396,800,346 | - | 118,198 | - | 510,186,312 |
| ILS | - | 347,562,683 | - | 117,022 | - | 506,951,594 |
| VNS | 345,706,679 | 375,109,092 | 116,604 | 116,728 | 505,906,031 | 506,957,910 |

ILS gave the best single aggregate on `Tai25b`. VNS produced the best recorded solution on `Sko90` and `Tai150b` and enabled a direct robustness study across its five runs. The largest `Tai150b` VNS experiment required more than twenty hours, illustrating why delta evaluation and explicit quick/full presets matter.

## Practice 2b

| Algorithm | Instance | Best | Mean | Worst | Population std. dev. | Evaluations per run |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Simple GA | Tai25b | 416,064,741 | 443,909,595 | 472,402,906 | 21,921,945 | 190,190 |
| CHC | Tai25b | 375,342,652 | 392,151,912 | 433,989,792 | 24,255,434 | about 10,450 |
| Multimodal GA | Tai25b | 379,819,176 | 394,514,998 | 404,378,194 | 10,444,881 | 50,050 |
| Simple GA | Sko90 | 124,884 | 125,660 | 127,196 | 902 | 190,190 |
| CHC | Sko90 | 128,818 | 129,655 | 130,088 | 492 | about 10,500 |
| Multimodal GA | Sko90 | 125,056 | 125,612 | 126,024 | 399 | 50,050 |
| Simple GA | Tai150b | 558,589,084 | 563,294,862 | 570,635,479 | 5,060,687 | 190,190 |
| CHC | Tai150b | 605,381,825 | 607,907,793 | 610,300,969 | 1,763,796 | 10,500 |
| Multimodal GA | Tai150b | 558,124,318 | 569,308,337 | 575,599,525 | 6,850,645 | 50,050 |

CHC used far fewer evaluations but was less competitive on the larger recorded instances. Clearing improved population diversity and produced the strongest average on `Tai25b`, while the Simple GA produced the strongest mean on `Tai150b`. The detailed run rows establish 128,818 as the best CHC value for `Sko90`.

## Final PSO project

The recorded final-project runs used 50 PSO updates, as shown by the evaluation count `30 + 50 x 30 = 1,530`. Local Search used 100 iterations and 1,001 evaluations.

| Algorithm | Best | Mean | Worst | Population std. dev. | Evaluations per run |
| --- | ---: | ---: | ---: | ---: | ---: |
| PSO, 50 updates | 0.000007 | 0.008840 | 0.040386 | 0.015825 | 1,530 |
| Local Search | 1.990919 | 5.972559 | 9.952645 | 3.017843 | 1,001 |

PSO found values several orders of magnitude closer to the global minimum and varied much less than Local Search. The package default is 100 PSO updates, matching the assignment and producing 3,030 evaluations per run. Seeded executions make the updated comparison directly reproducible.

### Reproducible 100-update reference run

The repository includes a second five-run comparison using seeds 0 through 4 and the assignment-compliant PSO budget.

| Algorithm | Best | Mean | Worst | Population std. dev. | Evaluations per run |
| --- | ---: | ---: | ---: | ---: | ---: |
| PSO, 100 updates | 5.32e-9 | 1.43e-7 | 6.68e-7 | 2.63e-7 | 3,030 |
| Local Search | 4.978308 | 17.514553 | 24.885075 | 9.067544 | 1,001 |

The exact per-run values, final coordinates, summary CSV, and figures are in [`results/reference/final-pso`](../results/reference/final-pso). They can be regenerated with the command shown in the main README.

## Interpreting the tables

These measurements describe particular parameter settings and seeds. They do not establish universal rankings among the algorithms. Runtime, objective evaluations, solution quality, and dispersion should be considered together, especially when comparing population methods with single-trajectory searches.
