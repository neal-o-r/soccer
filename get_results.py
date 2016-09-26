import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
from tqdm import tqdm


def get_results(home_goals, away_goals):


	df_mins = pd.read_csv('minutes.csv')
	df_res  = pd.read_csv('results.csv')

	mask = (df_res['home_goals']>=home_goals) & (df_res['away_goals']>=away_goals)

	print('%.2f%% matches had at least this score ' 
			%(mask.sum()/float(len(mask)) *100))


	df_redres = df_res[mask]
	
	hwins = (df_redres['home_goals'] > df_redres['away_goals']).sum()
	awins = (df_redres['home_goals'] < df_redres['away_goals']).sum()
	draws = mask.sum() - hwins - awins

	print("""Of those %d matches:\n 
		%d finished in a home win\n
		%d finished in an away win\n
		%d finished in a draw""" %(mask.sum(), hwins, awins, draws))
	


	hgoals = []
	agoals = []
	for row in tqdm(df_redres.iterrows()):

		date_mask  = df_mins['date'] == row[1].date
		team_mask1 = ((df_mins['scoring_team'] == row[1].home_team) & 
			      (df_mins['conceding_team'] == row[1].away_team)) 
		team_mask2 = ((df_mins['scoring_team'] == row[1].away_team) & 
			      (df_mins['conceding_team'] == row[1].home_team))			
		team_mask = team_mask1 | team_mask2	

		full_mask = date_mask & team_mask

		df_match = df_mins[full_mask]

		home_goalst = df_match[df_match.scoring_team == row[1].home_team].minute.values 
		away_goalst = df_match[df_match.scoring_team == row[1].away_team].minute.values
		
		if len(home_goalst)>home_goals: 
			hgoals.extend(home_goalst[home_goals+1:])
		if len(away_goalst)>away_goals:
			agoals.extend(away_goalst[away_goals+1:])		

	plt.hist(hgoals, bins=90, alpha=1, label='Home Goals')
	plt.hist(agoals, bins=90, alpha=1, label='Away Goals')
	plt.legend(loc='upper left')
	plt.show()
