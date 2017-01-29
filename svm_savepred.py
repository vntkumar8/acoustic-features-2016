from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(',')]
    return LabeledPoint(values[25], values[0:])

sc = SparkContext("local", "SVM-2")
data = sc.textFile("data1_out.csv")
parsedData = data.map(parsePoint)

(trainData, testData) = parsedData.randomSplit([0.7, 0.3])

# Build the model
model = SVMWithSGD.train(parsedData, iterations=100)

# Evaluating the model on training data
labelsAndPreds = trainData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(trainData.count())
print("Training Error = " + str(trainErr))

#Evaluating the model on test data
labelsAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
testErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(testData.count())
print("Test Error = " + str(testErr))


#Storing the predictions made in test data
def toCSVLine(data):
  return ','.join(str(d) for d in data)

lines = labelsAndPreds.map(toCSVLine)
lines.saveAsTextFile('labels-and-predictions2.csv')

# Save and load model
model.save(sc, "myModelPath")
sameModel = SVMModel.load(sc, "myModelPath")
