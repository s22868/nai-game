"""
Authors: Mateusz Budzyński, Igor Gutowski
dependencies:
    pip install tensorflow
    pip install seaborn
    pip install matplotlib
    pip install numpy
"""
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from tensorflow.python.ops.confusion_matrix import confusion_matrix

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Normalize the data
X_train = X_train / 255
X_test = X_test / 255

# encode labels

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build the model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model.add(MaxPooling2D())
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="softmax"))

# Build second model, more complex
model2 = Sequential()
model2.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model2.add(MaxPooling2D())
model2.add(Conv2D(64, (3, 3), activation="relu"))
model2.add(MaxPooling2D())
model2.add(Conv2D(128, (3, 3), activation="relu"))
model2.add(MaxPooling2D())
model2.add(Flatten())
model2.add(Dense(128, activation="relu"))
model2.add(Dropout(0.5))
model2.add(Dense(10, activation="softmax"))


# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model2.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))
model2.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))

# Evaluate the model
model.evaluate(X_test, y_test)
model2.evaluate(X_test, y_test)


# create confusion matrix
predictions = model.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)

y_test_labels = np.argmax(y_test, axis=1)
conf_matrix = confusion_matrix(y_test_labels, predicted_labels)

# plot and show confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=range(10), yticklabels=range(10))
plt.xlabel('Predicted')
plt.ylabel('Test')
plt.title('conf_matrix')
plt.show()

loss, accuracy = model.evaluate(X_test, y_test)

print(f"Loss model 1: {loss}")
print(f"Accuracy model 2: {accuracy}")

loss2, accuracy2 = model2.evaluate(X_test, y_test)

print(f"Loss model 2: {loss2}")
print(f"Accuracy model 2: {accuracy2}")

