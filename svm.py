from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext
from pyspark.mllib.util import MLUtils

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(',')]
    return LabeledPoint(values[13], values[0:4])

sc = SparkContext("local", "SVM")

#data = sc.textFile("svm_data.txt")
#parsedData = data.map(parsePoint)
trainData=MLUtils.loadLibSVMFile(sc, 'data/stripped.data')
testData=MLUtils.loadLibSVMFile(sc, 'data/stripped_test.data')

#	
#data = MLUtils.loadLibSVMFile(sc, "data/select.data", multiclass=False, numFeatures=-1, minPartitions=None)

#(trainData, testData) = data.randomSplit([0.7, 0.3])

# Build the model
model = SVMWithSGD.train(trainData, iterations=100, step=1.0, regParam=0.01, miniBatchFraction=1.0, initialWeights=None, regType='l1', intercept=False, validateData=True, convergenceTol=0.00001)
model.setThreshold(0.5)


#model=NaiveBayes.train(trainData, 1.0)

# Evaluating the model on training data
labelsAndPreds = trainData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(trainData.count())
print("Training Error = " + str(trainErr))

# Evaluating the model on test data
labelsAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
testErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(testData.count())
print("Test Error = " + str(testErr))



def toCSVLine(data):
  return ','.join(str(d) for d in data)

lines = labelsAndPreds.map(toCSVLine)
lines.saveAsTextFile('labels-and-predictions2.csv')

# Save and load model
model.save(sc, "myModelPath")
sameModel = SVMModel.load(sc, "myModelPath")

