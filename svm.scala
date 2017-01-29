// import neccessary libraries
import org.apache.spark.mllib.*
import org.apache.SparkContext

//loading training data(assume it to be pre processed)
val data = MLUtils.loadLibSVMFile(sc,"/path/to/file.dat")

val altData = sc.textFile("/path/to/data.dat")

//data splitting
val splits = data.randomsplit(Array(0.6,0.4),seed=1234L)
val training = splits(0)//.cache()
val test = splits(1)

//training
val epoch = 100
val model = SVMWithSGD.tarin(training,epoch)

//computing rwa scores on test set for evaluation
val scoresAndLabels = test.map {point =>
	val score = model.predict(point.features)
	(score.point.label)
}

//get evaluation metric
val metric = new BinaryClassificationMetrics(scoresAndLabels)
val auROC = metric.areaunderROC()

println("area under ROC is :: "+ auROC)