import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm

g_93h = np.loadtxt('serie93.csv', usecols=(4,), skiprows=1, delimiter=',') # read home goals scored in the Serie A in 93/94 season (2pts for a win)
g_94h = np.loadtxt('serie94.csv', usecols=(4,), skiprows=1, delimiter=',') # same for 94/95 and 95/96 (both 3pts for a win)
g_95h = np.loadtxt('serie95.csv', usecols=(4,), skiprows=1, delimiter=',')
g_99h = np.loadtxt('serie99.csv', usecols=(4,), skiprows=1, delimiter=',') # for the sake of comparison i also got 99/00

goals = np.r_[g_93h, g_94h, g_95h,g_99h] # concatenate into one set


''' 
We will model the number of goals scored per game by a Poisson process.
We begin with the assumption that the expected value is between 1 and 2, with a uniform prior distribution.
We only model home games, as away games will have a different expected value, though the model could be extended to account for this 
(constant offset, seperate lambdas...)
'''

lam1 = pm.Uniform("lam1", lower=1, upper=2) 
lam2 = pm.Uniform("lam2", lower=1, upper=2)
lam3 = pm.Uniform("lam3", lower=1, upper=2)
lam4 = pm.Uniform("lam4", lower=1, upper=2)

@pm.deterministic
def lambda_(lam1=lam1, lam2=lam2, lam3=lam3, lam4=lam4):
	# This function returns a lambda for each game, with a different lambda for each season.
	goals_lam = np.zeros(4*306)

	goals_lam[:306]         = lam1
	goals_lam[306:2*306]    = lam2
	goals_lam[2*306:3*306]  = lam3
	goals_lam[3*306:]       = lam4
	return goals_lam


observation = pm.Poisson("obs", lambda_, value=goals, observed=True)

model = pm.Model([observation, lam1, lam2, lam3, lam4])

mcmc = pm.MCMC(model)
mcmc.sample(50000, 10000, 2) # Run the model, 50000 samples, 10000 burn-in, thinning of 2.

lambda_1_samples = mcmc.trace('lam1')[:]
lambda_2_samples = mcmc.trace('lam2')[:]
lambda_3_samples = mcmc.trace('lam3')[:]
lambda_4_samples = mcmc.trace('lam4')[:]

# Plot histograms of the posterior samples.
plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.75, label="posterior of $\lambda_{93}$", color="#A60628")

plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.75, label="posterior of $\lambda_{94}$", color="#7A68A6")

plt.hist(lambda_3_samples, histtype='stepfilled', bins=30, alpha=0.75, label="posterior of $\lambda_{95}$", color="#467821")

plt.hist(lambda_4_samples, histtype='stepfilled', bins=30, alpha=0.75, label="posterior of $\lambda_{99}$", color="#348ABD")

plt.legend(loc="upper left")
plt.title(r"""Posterior distributions of the variables $\lambda_{93},\;\lambda_{94},\;\lambda_{95},\;\lambda_{99}$""")
plt.xlim([1, 2])
plt.xlabel("Value of $\lambda_i$")
plt.ylabel("Number of Samples")


#plt.savefig("lambdas.png")


