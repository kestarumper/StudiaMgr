import scala.io.Source
import java.io.FileWriter
import java.io.BufferedWriter
import java.io.File

object Main {
  def writeFile(filename: String, lines: Seq[String]): Unit = {
    val file = new File(filename)
    val bw = new BufferedWriter(new FileWriter(file))
    for (line <- lines) {
        bw.write(line + "\n")
    }
    bw.close()
  }

  def main(args: Array[String]): Unit = {
    val fileName = "illiad.txt"
    val fileNameStopWords = "./stopwords_en.txt"

    val fileStopWords = Source.fromFile(fileNameStopWords, "UTF-8")
    val stopWords = fileStopWords.mkString.split("\\s+")
    fileStopWords.close

    val file = Source.fromFile(fileName, "UTF-8")
    val words = file.mkString
      .split(("\\s+"))
      .toList
      .map(word => (word.toLowerCase
        .replaceAll("[^\\w]+$", "")
        .replaceAll("^[^\\w]+", "")
      ))
      .filter(word => word.length > 0)
      .filterNot(stopWords.contains)
      .map(word => (word, 1))

    val grouped = words.groupBy(x => x._1)
    val reduced = grouped.mapValues(x => x.length)
    val sorted = reduced.toSeq.sortWith((a, b) => a._2 > b._2).take(1000)

    for (word <- sorted) {
      println(word)
    }
    file.close

    writeFile("wordcloud.csv", sorted.map(x => x._2 + "," + x._1))
  }
}