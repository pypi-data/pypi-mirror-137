# kep\_solver

This Python package is devoted to various algorithms, procedures and mechanisms
that are useful when studying kidney exchange programmes in general.  It is
written and maintained by [William Pettersson](mailto:william.pettersson@glasgow.ac.uk)

## Quick start

Create a virtual environment for kep\_solver

    mkvirtualenv kep_solver

Install kep\_solver

    pip install kep_solver

Download a sample JSON file from
`https://kep-web.optimalmatching.com/static/jsons/sample-1.json`

Run the following Python commands

```python
# Import the required functions
from kep_solver.fileio import read_json
from kep_solver.pool import Pool
from kep_solver.model import TransplantCount

# Read some input
instance = read_json("sample-1.json")

# Create a transplant pool with one objective
pool = Pool([TransplantCount()])

# Cycles can have at most 3 donor/recipient pairs, and chains can have at most
# 2 donors (i.e., one non-directed donor and one donor/recipient pair)
solution = pool.solve_single(instance, maxCycleLength=3, maxChainLength=2)

# Print the solution
for selected in solution.selected:
    print(f"Selected {selected}")
```

## Current features

* Reading instance files (json and XML formats)
* Creation of compatibility graphs
* Solving for the following objectives (single, or hierarchical)

    * Maximise the number of transplants
    * Maximise the number of backarcs
    * Maximise the number of effective 2-way exchanges
    * Minimise the number of three-cycles
    * Maximise the score using the UK scoring mechanisms

While the above objectives are exactly those in use by NHSBT when running the UKLKSS (the UK national KEP), I do intend to add further objectives

## Expected users

I see two classes of users of this software:

* Researchers - Depending on what questions you want answered, you can either test policy changes to determine how they affect the running of a KEP, or you can implement new models or objectives to see how they perform
* Health care institutes - I have tried to make this software as robust as possible, but for now I cannot guarantee any particular level of performance or any exact optimality of a solution. If you do want to use this software for real-world impact, feel free to get in touch and I may be able to help.

## Interface

This is just a Python module for now, a web-interface that demonstrates a basic
use case is viewable at
[https://kep-web.optimalmatching.com](https://kep-web.optimalmatching.com), and
the source code for said website is online at
[https://gitlab.com/wpettersson/kep\_web](https://gitlab.com/wpettersson/kep_web)

## Future plans

* More objective functions
* Random instance generation
* Simulating the development of a KEP over time
* Supporting transnational pools
* Implementation of faster models and modelling techniques


## Contributing

I welcome input from others, whether you have ideas for improvements or want to
submit code. Either get in touch directly, or raise an
[issue](https://gitlab.com/wpettersson/kep_solver/-/issues)

## Acknowledgements

This software has been supported by the Engineering and Physical Sciences
Research Council (EPSRC) grant
[EP/T004878/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/T004878/1)
(Multilayer Algorithmics to Leverage Graph Structure).
