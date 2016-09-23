import pandas as pd

df_min = pd.read_csv('minutes.csv')
df_res = pd.read_csv('results.csv')


d = {'Home_goals':None, 'Away_goals':None, 'Times':None, 'Winners':None}
df_final = pd.DataFrame(data=d, index=range(0))
for row in df_res.iterrows():
        
        row = row[1]       
 
        home_team = row.home_team    
        away_team = row.away_team
        date      = row.date

        date_mask  = df_mins['date'] == date
        team_mask1 = ((df_mins['scoring_team'] == home_team) & 
                              (df_mins['conceding_team'] == away_team)) 
        team_mask2 = ((df_mins['scoring_team'] == away_team) & 
                              (df_mins['conceding_team'] == home_team))                  
        mask = team_mask1 | team_mask2     

        full_mask = date_mask & team_mask

        df_match = df_mins[full_mask]

        

