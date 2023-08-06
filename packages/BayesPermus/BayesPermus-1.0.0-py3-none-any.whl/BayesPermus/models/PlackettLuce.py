from .Base import Base

import numpy as np
import pystan

pld_code = """
data {
    int<lower=1> num_permus;
    int<lower=2> num_algorithms;
    int permus [num_permus, num_algorithms];
    vector[num_algorithms] alpha;
}

parameters {
    simplex[num_algorithms] ratings;
}
 
transformed parameters {
  real loglik;
  real rest;
  
  loglik = 0;
  for (s in 1:num_permus){
    for (i in 1:(num_algorithms - 1)) {
      rest = 0;

      for (j in i:num_algorithms) {
        rest = rest + ratings[permus[s, j]];
      }

      loglik = loglik + log(ratings[permus[s, i]] / rest);
    }
  }
}
 
model {
    ratings ~ dirichlet(alpha);
    target += loglik;
}
"""

class PlackettLuceDirichlet(Base):
  """ The Plackett-Luce model using a Dirichlet prior.
  """

  def __init__(self, alpha, seed=1, num_chains=1, num_samples=2000):
    Base.__init__(self, stan_model=pld_code, 
                  seed=seed, num_chains=num_chains, num_samples=num_samples)
    self.alpha = alpha    

  def get_model_data(self, permus):
    num_permus, num_algorithms = permus.shape
    model_data = {'num_permus': num_permus,
                  'num_algorithms': num_algorithms,
                  'permus': permus,
                  'alpha': self.alpha}
    return model_data

  def calculate_permu_prob(self, permu, params):
    num_algorithms = len(permu)
    ratings = params
    prob = 1

    for i in range(num_algorithms):
      denominator = np.sum([ratings[permu[j]] for j in range(i, num_algorithms)])
      prob *= ratings[permu[i]] / denominator

    return prob


plg_code = """
data {
    int<lower=1> num_permus;
    int<lower=2> num_algorithms;
    int permus [num_permus, num_algorithms]; 
    real alpha; 
    real beta;
}

parameters {
    simplex[num_algorithms] ratings;
}
 
transformed parameters {
  real loglik;
  real rest;
  
  loglik = 0;
  for (s in 1:num_permus){
    for (i in 1:(num_algorithms - 1)) {
      rest = 0;

      for (j in i:num_algorithms) {
        rest = rest + ratings[permus[s, j]];
      }

      loglik = loglik + log(ratings[permus[s, i]] / rest);
    }
  }
}
 
model {
    for (i in 1:num_algorithms) {
        ratings[i] ~ gamma(alpha, beta);
    }

    target += loglik;
}
"""

class PlackettLuceGamma(Base):
  """ The Plackett-Luce model using a Gamma prior.
  """

  def __init__(self, alpha, beta, seed=1, num_chains=1, num_samples=2000):
    Base.__init__(self, stan_model=plg_code, 
                  seed=seed, num_chains=num_chains, num_samples=num_samples)
    self.alpha = alpha
    self.beta = beta  

  def get_model_data(self, permus):
    num_permus, num_algorithms = permus.shape
    model_data = {'num_permus': num_permus,
                  'num_algorithms': num_algorithms,
                  'permus': permus,
                  'alpha': self.alpha,
                  'beta': self.beta}
    return model_data

  def calculate_permu_prob(self, permu, params):
    num_algorithms = len(permu)
    ratings = params
    prob = 1

    for i in range(num_algorithms):
      denominator = np.sum([ratings[permu[j]] for j in range(i, num_algorithms)])
      prob *= ratings[permu[i]] / denominator

    return prob
