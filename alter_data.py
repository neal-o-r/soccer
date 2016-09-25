import pandas as pd
from tqdm import tqdm

df_min = pd.read_csv('minutes.csv')
df_res = pd.read_csv('results.csv')


d = {'home_score':None, 'away_score':None, 'time':None, 'winners':None}
df_final = pd.DataFrame(data=d, index=range(0))

i = 0
j = 0
for row in tqdm(df_res.iterrows()):
        
        row = row[1]       

	if row.home_goals == 0 and row.away_goals == 0:
		continue
	
        home_team = row.home_team    
        away_team = row.away_team
	date      = row.date

	if row.home_goals > row.away_goals:

		winners = 1
	elif row.away_goals > row.home_goals:

		winners = -1
	else:

		winners = 0


	date_mask = df_min['date'] == date
        team_maskh = ((df_min['scoring_team'] == home_team) & 
                              (df_min['conceding_team'] == away_team)) 
        team_maska = ((df_min['scoring_team'] == away_team) & 
                              (df_min['conceding_team'] == home_team))         

	team_mask = team_maska | team_maskh     

        full_mask = date_mask & team_mask
	sub_frame = df_min[full_mask]
		
	home_score, away_score = 0, 0
	for sub_row in sub_frame.iterrows():
		sub_row = sub_row[1]

		if sub_row.scoring_team == home_team:
			home_score += 1
		if sub_row.scoring_team == away_team:
			away_score += 1

		df_final.loc[i] = [home_score, away_score, sub_row.minute, winners]

		i += 1
