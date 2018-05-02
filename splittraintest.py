import numpy as np
import pandas as pd
import sys
## run program as python splittraintest.py (path to file) (percentage for training)
## e.x. python splittraintest.py data/parkinglot_labels.csv 0.8
## the above line will split your csv of all labels into two csv's one being train_labels and the other test_labels where 80% is in the training set 
def main():
	np.random.seed(1)
	if sys.argv < 2:
		print("Incorrect Number of Arguments")
		return
	labels = pd.read_csv(sys.argv[1])
	groups = labels.groupby('filename')
	grouped_list = [groups.get_group(x) for x in groups.groups]
	train_index = np.random.choice(len(grouped_list), size=int(len(grouped_list)*float(sys.argv[2])), 	replace=False)
	test_index = np.setdiff1d(list(range(len(grouped_list))),train_index)
	train = pd.concat([grouped_list[i] for i in train_index])
	test = pd.concat([grouped_list[i] for i in test_index])
	train.to_csv('train_labels.csv', index=None)
	test.to_csv('test_labels.csv', index=None) 
	print("Toal number of labels: " + len(grouped_list))
	print("Number of training elements: " + len(train_index)) 
	print("Number of testing elements: " + len(test_index))

main()
