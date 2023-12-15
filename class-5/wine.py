"""
Authors: Mateusz Budzyński, Igor Gutowski

dependencies:
    pip install sklearn
    pip install tensorflow
"""

from sklearn import datasets
from sklearn.model_selection import train_test_split 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout

#load dataset

wine = datasets.load_wine()

#x - data (alcohol, malic_acid) y - target (class ---- 0, 1, 2)
X = wine.data[:, :2]
y = wine.target

#split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Build the model
model = Sequential()
model.add(Flatten()),
model.add(Dense(128, activation="relu")),
model.add(Dense(10, activation="softmax"))

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
model.fit(X_train, y_train, epochs=40, verbose=1, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Loss:", loss)
print("Accuracy:", accuracy)