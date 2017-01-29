

"""
Decision Tree Regression Example.
"""
from __future__ import print_function

from pyspark import SparkContext
# $example on$
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils
# $example off$

if __name__ == "__main__":

    sc = SparkContext(appName="PythonDecisionTreeRegressionExample")

    # $example on$
    # Load and parse the data file into an RDD of LabeledPoint.
    #data = MLUtils.loadLibSVMFile(sc, 'data/mllib/sample_libsvm_data.txt')
    # Split the data into training and test sets (30% held out for testing)
    #(trainingData, testData) = data.randomSplit([0.7, 0.3])
    trainingData=MLUtils.loadLibSVMFile(sc, 'data/xaa')
    testData=MLUtils.loadLibSVMFile(sc, 'data/xab')
    # Train a DecisionTree model.
    #  Empty categoricalFeaturesInfo indicates all features are continuous.
    model = DecisionTree.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
                                     impurity='gini', maxDepth=10, maxBins=1024)

    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
    print('Test Error = ' + str(testErr))
#    testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
#    print('Test Mean Squared Error = ' + str(testMSE))
    print('Learned regression tree model:')
    print(model.toDebugString())

    # Save and load model
    model.save(sc, "target/tmp/myDecisionTreeRegressionModel")
    sameModel = DecisionTreeModel.load(sc, "target/tmp/myDecisionTreeRegressionModel")
    # $example off$

