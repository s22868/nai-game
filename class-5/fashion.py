from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout


(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# normalize data
X_train = X_train / 255
X_test = X_test / 255

# Build the model
model = Sequential()
model.add(Flatten(input_shape=(28, 28))),
model.add(Dense(128, activation="relu")),
model.add(Dropout(0.5)),
model.add(Dense(10, activation="softmax"))

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Loss:", loss)
print("Accuracy:", accuracy)
