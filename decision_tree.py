# %%
import numpy as np
import matplotlib.pyplot as plt


age = np.array([26, 16, 99, 97, 67, 66,  9, 14, 39, 45, 39, 62, 14, 42, 24, 99, 64,
       21, 74, 58, 99, 56, 51, 14, 79,  7, 77, 89, 20, 72, 81, 41, 76, 58,
        2, 15,  0, 84, 38, 53, 82, 23, 88, 69, 12,  8, 43, 91, 75, 82, 20,
       47, 57, 88, 53, 86, 93, 90, 45, 52, 94, 36, 97, 95, 92, 60, 70, 31,
       27, 84, 65, 35, 13, 28, 15, 68, 43, 78, 34, 71, 78, 41, 38, 31, 12,
       68, 12, 71, 52, 64, 25, 95, 46, 19, 95, 99, 96, 31, 18, 15])
grey_hair = np.array([False, False, False, False,  True,  True,  True, False, False,
        True, False,  True, False,  True, False, False,  True, False,
        True,  True, False,  True,  True, False,  True,  True,  True,
        True, False,  True,  True,  True,  True,  True,  True, False,
        True,  True, False,  True,  True, False,  True,  True, False,
        True,  True, False,  True,  True, False,  True,  True,  True,
        True,  True, False, False,  True,  True, False, False, False,
       False, False,  True,  True, False, False,  True,  True, False,
       False, False, False,  True,  True,  True, False,  True,  True,
        True, False, False, False,  True, False,  True,  True,  True,
       False, False,  True, False, False, False, False, False, False,
       False])

# Plot the points
plt.scatter(age, grey_hair, c=grey_hair)
# %%

def entropy(inputs):
    counts = np.bincount(inputs)
    if len(counts) <= 1:
        return 0.
    
    return 1. - abs(counts[0]-counts[1]) / len(inputs)
# %%

intial_entropy = entropy(grey_hair)

best_entropy = intial_entropy

best_split = None

for split_point in age:
    left = age < int(split_point)
    right = age > int(split_point)

    left_entropy = entropy(left)
    right_entropy = entropy(right)

    current_entropy = left_entropy + right_entropy

    if current_entropy < best_entropy:
        best_entropy = current_entropy
        best_split = split_point

#print("Best split point is at:", best_split, "with a entropy of:", best_entropy)


## PROBLEM: Current best entropy is at split position 0? Should be an age, not 0.


#Chaos, Vermischung, Diversion, Entropy minimieren, Einheitlichkeit maximieren:

# Entropy-Wert: soll hoch sein, wenn wir viele verschiedene Klassen vertreten, Extremwert bei 50/50
# soll klein/minimal sein, wenn wir eine einzige Klasse haben (0 bei 100%)

# Einheitlichkeit = abs(Anzahl NG - Anzahl G) / Anzahl Elemente

# Entropy = 1 - Einheitlichkeit
#     = 1 - (abs(Anzahl NG - Anzahl G) / Anzahl Elemente)




# %%
