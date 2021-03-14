import java.io.{File, FileWriter}
import scala.io.Source.fromFile
import scala.util.Sorting

case class Coordinate(latitude: Double, longitude: Double) {
  def distanceTo(coordinate: Coordinate): Double = {
    val diffLatitude = coordinate.latitude - latitude
    val diffLongitude = coordinate.longitude - longitude
    math.sqrt(diffLatitude * diffLatitude + diffLongitude * diffLongitude)
  }

  override def toString: String = s"$latitude, $longitude"
}

case class CsvRow(key: String, location: String, coordinate: Coordinate)

object Main extends App {
  def test1(): Unit = {
    val filename = "/home/user/scala/Uni/data/geodata.csv"
    val dataList: Array[(String, Coordinate, String)] = fromFile(filename).getLines.drop(1).map { line =>
      val lineSplit = line.split(",")
      val key = lineSplit(3)
      val latitudeIndex = lineSplit.length - 4
      val longitudeIndex = lineSplit.length - 3
      val latitude = lineSplit(latitudeIndex).toDouble
      val longitude = lineSplit(longitudeIndex).toDouble
      (key, Coordinate(latitude, longitude), line.split(",").slice(17, 22).mkString(""))
    }.toArray

    val forCopy = dataList.clone()
    for((key, coordinate, _) <- dataList.take(5)) {
      Sorting.quickSort(forCopy)(new Ordering[(String, Coordinate, String)] {
        override def compare(lhs: (String, Coordinate, String), rhs: (String, Coordinate, String)): Int = {
          if(lhs._2.distanceTo(coordinate) - rhs._2.distanceTo(coordinate) > 0) 1
          else -1
        }
      })
      println(forCopy.slice(1, 6).foldLeft(key)((acc, el) => acc + "," + el._1 + "," + el._3))
    }
  }

  // Point, location, latitude, longitude -> Point, location
  def test2(): Unit = {
    val definedLocationRows: Array[CsvRow] = fromFile("/home/user/scala/Uni/data/centers.csv").getLines.drop(1).map { line =>
      val Array(key, location, latitude, longitude) = line.split('|')
      CsvRow(key, location, Coordinate(latitude.toDouble, longitude.toDouble))
    }.toArray

    var dataList: Array[(String, Coordinate)] = fromFile("/home/user/scala/Uni/data/geodata.csv").getLines.drop(1).map { line =>
      val lineSplit = line.split(",")
      val key = lineSplit(3)
      val latitudeIndex = lineSplit.length - 4
      val longitudeIndex = lineSplit.length - 3
      val latitude = lineSplit(latitudeIndex).toDouble
      val longitude = lineSplit(longitudeIndex).toDouble
      (key, Coordinate(latitude, longitude))
    }.toArray

    val destinationFile = "/home/user/scala/Uni/data/matchinglocation.csv"
    val fileWriter = new FileWriter(new File(destinationFile))
    for (row <- definedLocationRows) {
      Sorting.quickSort(dataList)(new Ordering[(String, Coordinate)] {
        override def compare(lhs: (String, Coordinate), rhs: (String, Coordinate)): Int =
          if(lhs._2.distanceTo(row.coordinate) - rhs._2.distanceTo(row.coordinate) > 0) 1
          else -1
      })

      println("[start matching]..")
      val matched = dataList.takeWhile { case (_, c) => c.distanceTo(row.coordinate) <= 0.25 }
      dataList = dataList.drop(matched.length)
      println(s"[matched]: ${matched.length}")
      println(s"[rows left after matching]: ${dataList.length}")
      matched.foreach(m => {
        fileWriter.write(s"${m._1},${row.key}\n")
      })
    }
  }

  test2()
}