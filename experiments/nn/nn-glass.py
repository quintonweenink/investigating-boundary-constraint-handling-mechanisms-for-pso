import matplotlib.pyplot as plt
import numpy as np

from mlpy.dataSet.dataSetTool import DataSetTool
from mlpy.numberGenerator.bounds import Bounds
from mlpy.neuralNetwork.feedForwardNeuralNetwork import NeuralNetwork
from mlpy.neuralNetwork.structure.layer import Layer

np.set_printoptions(suppress=True)

dataSetTool = DataSetTool()
training, testing, generalization= dataSetTool.getGlassDataSets('../../dataSet/glass/glass.data')

l_rate = 0.01

bounds = Bounds(-2, 2)

inputLayer = Layer(bounds, size = len(training[0][0]), prev = None, l_rate = l_rate, bias = True, label = "Input layer")
hiddenLayer = Layer(bounds, size = 12, prev = inputLayer, l_rate = l_rate, bias = True, label = "Hidden layer")
outputLayer = Layer(bounds, size = len(training[0][1]), prev = hiddenLayer, l_rate = l_rate, bias = False, label = "Output layer")

fnn = NeuralNetwork()
fnn.appendLayer(inputLayer)
fnn.appendLayer(hiddenLayer)
fnn.appendLayer(outputLayer)

group_training = np.array([input[0] for input in training])
group_target = np.array([output[1] for output in training])

errors = []

plt.grid(1)
plt.xlabel('Iterations')
plt.ylabel('Error')
plt.ylim([0, 1])
plt.ion()

for i in range(5000):
    result = fnn.fire(group_training)
    i_error = fnn.backPropagation(group_target)

    difference = group_target - result
    fnn.error = np.mean(np.square(difference))

    if i % 100 == 0:
        errors.append(fnn.error)
        plt.scatter(i, abs(fnn.error), color='blue', s=4, label="test1")
        plt.pause(0.0001)
        plt.show()

correct = 0

for i in range(len(generalization)):
    in_out = generalization[i]
    result = fnn.fire(np.array([in_out[0]]))

    if np.argmax(result) == np.argmax(in_out[1]):
        correct += 1


print("Classification accuracy: ")
print(str(correct/len(generalization)) + "%")

