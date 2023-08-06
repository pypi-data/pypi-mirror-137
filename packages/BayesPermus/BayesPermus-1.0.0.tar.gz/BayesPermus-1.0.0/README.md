# BayesPermus

Bayesian inference of algorithm performance using permutation models.

## Installation

```
pip install BayesPermus
```

## Usage

1. Prepare permutation data:

```python
permus = np.array([[1,2,3], [1,3,2]])
```

2. Obtain the marginal probabilities:

```python
from BayesPermus.models.BradleyTerry import BradleyTerry

# BT Dirichlet hyper-priors
dirichlet_alpha_bt = [1, 1, 1]

# Create Bayesian inference model
bradleyTerry = BradleyTerry(dirichlet_alpha_bt, num_samples=1000)

# Calculate the marginal probabilities
probs = bradleyTerry.calculate_top_ranking_probs(permus)

```

## Additional available models

* Bradley-Terry:
```python
from BayesPermus.models.BradleyTerry import BradleyTerry
```
* Plackett-Luce:
```python
from BayesPermus.models.PlackettLuce import PlackettLuceDirichlet
from BayesPermus.models.PlackettLuce import PlackettLuceGamma
```

* Mallows Model:
```python
from BayesPermus.models.MallowsModel import MallowsModel
```

## Additional available marginals

* Probability of an algorithm to be in the first position: `model.calculate_top_ranking_probs(...)`.
* Probability of an algorithm to outperform another: `model.calculate_better_than_probs(...)`.
* Probability of an algorithm to be in the top-k ranking: `model.calculate_top_k_probs(...)`.