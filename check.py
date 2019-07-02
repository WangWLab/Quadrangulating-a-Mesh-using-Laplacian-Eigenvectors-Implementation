import pickle
with open('evecs.pkl', 'rb') as f:
    data = pickle.load(f)
print(data)
print(data[:, 0])