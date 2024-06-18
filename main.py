# %%

import numpy as np
import matplotlib.pyplot as plt

# Generate two feature arrays, together presenting a grid of points with the size of 5x5
bounds = 5, 5
n_points = 500
x1, x2 = np.meshgrid(
    np.linspace(-bounds[0], bounds[0], n_points), 
    np.linspace(-bounds[1], bounds[1], n_points))

# Flatten the arrays to get a list of points
x1 = x1.flatten()
x2 = x2.flatten()

# categorise the points into two classes, inside and outside of a circle
radius = 3
c = (x1**2 + x2**2 < radius**2).astype(int)

# Plot the points
class Tree:
    def __init__(self, depth, labels):
        self.depth = depth
        self.left = None
        self.right = None
        self.split_dim = None
        self.split_value = None
        self.labels = labels
        self.one_label = None

    @staticmethod
    def entropy(classes):
        # low if all classes are the same:
        # high if all classes are diverse:
        counts = np.bincount(classes)
        if len(counts) <= 1:
            return 0.

        return 1. - abs(counts[0]-counts[1])/len(classes)

    def fit(self, x, targets):
        classes, counts = np.unique(targets, return_counts=True)
        if self.depth == 0 or len(classes) == 1:
            self.one_label = classes[np.argmax(counts)]
            return

        # find best split:
        best_entropy = None
        best_dim = None
        best_split_value = None
        best_is_left = None
        for dim in range(x.shape[1]):
            if np.equal(x[:, dim], x[0, dim]).all():
                continue

            split_value = np.median(x[:, dim])
            is_left = x[:, dim] < split_value
            entropy = self.entropy(targets[is_left])+self.entropy(targets[~is_left])
            if best_entropy is None or entropy < best_entropy:
                best_dim = dim
                best_split_value = split_value
                best_is_left = is_left
                best_entropy = entropy

        if best_dim is None:
            self.one_label = classes[np.argmax(counts)]
            return

        self.split_dim = best_dim
        self.split_value = best_split_value

        self.left = Tree(self.depth - 1, self.labels)
        self.left.fit(x[best_is_left], targets[best_is_left])

        self.right = Tree(self.depth - 1, self.labels)
        self.right.fit(x[~best_is_left], targets[~best_is_left])

    def predict(self, x):
        if self.one_label is not None:
            return self.one_label

        if x[self.split_dim] < self.split_value:
            return self.left.predict(x)
        else:
            return self.right.predict(x)

def draw(x1, x2, c):
    plt.figure(figsize=(10, 10))
    plt.scatter(x1, x2, c=c)
    plt.scatter(x1, x2, c=c_pred, marker='.', alpha=0.8)

inputs = np.column_stack([x1, x2])

tree = Tree(50, labels=[0, 1])
tree.fit(inputs, c)
c_pred = np.array([tree.predict([i, j]) for i, j in zip(x1, x2)])

# calculate the accuracy of the model
accuracy = (c == c_pred).mean()
print(f"Accuracy: {accuracy}")

# %%
