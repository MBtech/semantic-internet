#!/bin/bash

python -m plots.boxplot 

python -m plots.plot_relevant_context triviaqa individual
python -m plots.plot_relevant_context hotpotqa individual
python -m plots.plot_relevant_context truthfulqa individual

python -m plots.plot_relevant_context triviaqa global
python -m plots.plot_relevant_context hotpotqa global
python -m plots.plot_relevant_context truthfulqa global