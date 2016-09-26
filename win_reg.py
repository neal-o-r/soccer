import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score
import patsy as pt
import numpy as np

def win_logit(home_score, away_score, time, team='home'):

	df = pd.read_csv('logit_data.csv')

	if team == 'away':
		
		df.winners = -1 * df.winners
	
	df.winners = (df.winners + abs(df.winners)) / 2	

	y, X = pt.dmatrices('winners ~ home_score + away_score + time',
                  df, return_type="dataframe")


	y = np.ravel(y)

	model = LogisticRegression()
	model = model.fit(X, y)

	scores = cross_val_score(LogisticRegression(), X, y, scoring='accuracy', cv=10)
	print "The cross-validated model score is: %.2f%%" %(100*scores.mean())


        features = [1, home_score, away_score, time]   
        features = np.array(features).reshape((1,-1))    
        
        results =  model.predict_proba(features)
	print("Given a score of %d - %d at %d minutes, the probability of the %s team winning is %.2f%%"
		%(home_score, away_score, time, team, 100*results[0][1]))	



if __name__ == '__main__':

	win_logit(1, 3, 30)
