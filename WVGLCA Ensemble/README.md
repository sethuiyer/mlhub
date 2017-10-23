### WVGLAE Ensemble 

An ensemble learning approach where ensembles are assumed to be in a weighted voting game.  At each test point, we find the nearest 5 points in validation set and measure the accuracy of these individual classifiers in that neighborhood and assign weight accordingly.

This method is effective when there is very less training data and we have number of weak learners which perform moderately on test data. This method is known as *Weighted voting game using Local accuracy estimates*.