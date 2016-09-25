# Soccer

Some simple analysis of the results of soccer matches. In the top directory, there's a piece of code which searches a (very cumbersomely formatted) set of ~8000 match results, and returns, from given a scoreline, when goals were scored. It also contains a simple Logitstic Regression model that, given a score-line and a time, returns the liklihood one or the other team will win.

The second piece of analysis examines that hypothesis that the change from 2-points for a win to 3-points for a win altered the way teams played, specifically how many goals were scored per game. To examine this I took data from the Serie A before and after the rule change (the Serie A being the last major league to make this transition, they did so in 1994), and examined the results. I modelled the number of goals per game as a Poisson process, and using PYMC produced a Bayesian model of the Expected Goals per Game. This analysis is pretty straightforward, but it showed no real difference in the Expected Goals per Game before and after the rule change, with a KL divergence of ~0.002. 

![Poisson](https://github.com/neal-o-r/soccer/blob/master/goals/posterior.png)
