
import matplotlib.pyplot as plt
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from numpy import loadtxt
import numpy as np


### INSERT ALL OF YOUR CODE HERE
def train_model():
	# load the training dataset
	dataset = loadtxt('wine_training.csv', delimiter=',')
	# split into input (X) and output (y) variables
	X = dataset[:,1:]
	y = dataset[:,0]
	print(y)
	y = to_categorical(y)

	# define the keras model
	model = Sequential()
	model.add(Dense(12, input_dim=13, activation='relu'))
	model.add(Dense(12, activation = 'relu'))
	model.add(Dense(4, activation= 'softmax'))

	# compile the keras model
	model.compile(loss = 'categorical_crossentropy',optimizer = 'adam', metrics =['accuracy'])

	# fit the keras model on the dataset
	model.fit(X,y,epochs=150, batch_size=13, verbose=1)

	return model


### DON'T MODIFY ANY CODE HERE
def eval_model(model):

	# load the testing dataset
	dataset = loadtxt('wine_test.csv', delimiter=',')
	print(type(dataset))

	# split into input (X) and output (y) variables
	X = dataset[:, 1:]
	y = dataset[:, 0]
	y = to_categorical(y)

	# PREDICTIONS & EVALUATION

	# Final evaluation of the model
	scores = model.evaluate(X, y, verbose=0)
	print("Baseline Error: %.2f%%" % (100 - scores[1] * 100))
	# predict first 4 images in the test set
	print("First 4 predictions:", model.predict(X[:4]))
	# actual results for first 4 images in test set
	print("First 4 actual classes:", y[:4])

	# make class predictions with the model
	predictions = model.predict_classes(X)

	# summarize the first 5 cases
	for i in range(5):
		print('%s => %d ' % (X[i].tolist(), predictions[i]), '(expected ', y[i], ')')



if __name__ == '__main__':
	model = train_model()
	eval_model(model)
