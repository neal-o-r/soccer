import re
import pandas as pd
import matplotlib.pyplot as plt

def searcher(h_g, a_g):
	# input a home score and an away score,
	# this returns the outcomes from games with at least this scoreline
	# and a histogram of when home and away goals were scored from this scoreline
	h_g = str(h_g)
	a_g = str(a_g)


	games = []
	htw   = []
	atw   = []
	draw  = []
	for line in open('results.csv'):
		if re.match('.*['+h_g+'-9],['+a_g+'-9].*', line):
			games.append(line)
		
			if (line.split(',')[2] > line.split(',')[3]):
				htw.append(line)
		
			if (line.split(',')[3] > line.split(',')[2]):
				atw.append(line)
		
			if (line.split(',')[2] == line.split(',')[3]):
				draw.append(line)	

	n_of_g = len(games) # no. of matches that had that score
	n_of_h = len(htw)   # no. of games the home team went on to win
	n_of_a = len(atw)   # away teams
	n_of_d = len(draw)  # no of draws

	h_g_min = []
	a_g_min = []

	df = pd.read_csv('minutes.csv')

	for game_w_goal in (htw + atw + draw):
	
		name_h = game_w_goal.split(',')[0]
		name_a = game_w_goal.split(',')[1]
		date   = game_w_goal.split(',')[-1][:-1]

		if (game_w_goal.split(',')[2] > h_g) and (game_w_goal.split(',')[2] != game_w_goal.split(',')[3]):# home team scored (again)
			dummy = df[(df.scoring_team == name_h) & (df.conceding_team == name_a) & (df.date==date)].minute.values 
			h_g_min.extend(dummy[int(h_g):])
	
		if (game_w_goal.split(',')[3] > a_g) and (game_w_goal.split(',')[2] != game_w_goal.split(',')[3]): # away team scored (again)
			dummy = df[(df.scoring_team == name_a) & (df.conceding_team == name_h) & (df.date==date)].minute.values 
			a_g_min.extend(dummy[int(a_g):])
	
		if (game_w_goal.split(',')[3] > a_g) and (game_w_goal.split(',')[2] == game_w_goal.split(',')[3]):
			dummy = df[(df.scoring_team == name_a) & (df.conceding_team == name_h) & (df.date==date)].minute.values 
			a_g_min.extend(dummy[int(a_g):])
			
			dummy = df[(df.scoring_team == name_h) & (df.conceding_team == name_a) & (df.date==date)].minute.values 
			h_g_min.extend(dummy[int(h_g):])

# Now we can plot histograms of when any goals were scored after the input score-line
	plt.hist(h_g_min, bins=90) 
	plt.savefig('hg_hist.png')
	plt.clf()

	plt.hist(a_g_min, bins=90) 
	plt.savefig('ag_hist.png')
	plt.clf()
	print 'In games with at least this score line, home teams won %d of %d matches in our data set, away teams won %d, and %d ended in a draw' %(n_of_h, n_of_g, n_of_a, n_of_d)

