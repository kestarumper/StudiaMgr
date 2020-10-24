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

  def countWords(
      input: String,
      stopWords: Array[String]
  ): Seq[(String, Int)] = {
    val words = input
      .split(("\\s+"))
      .toList
      .map(word =>
        (word.toLowerCase
          .replaceAll("[^\\w]+$", "")
          .replaceAll("^[^\\w]+", ""))
      )
      .filter(word => word.length > 0)
      .filterNot(stopWords.contains)
      .map(word => (word, 1))

    val grouped = words.groupBy(x => x._1)
    val reduced = grouped.mapValues(x => x.length)

    return reduced.toSeq;
  }

  def getChapters(input: String): Seq[(String, String)] = {
    val pattern = "####-\\s*\\n*(Chapter \\d+\\.?(\\s[\\w-]+)*)"
    val re = pattern.r;
    val chapters = re.findAllIn(input).matchData.map(m => m.group(1)).toSeq
    return chapters.zip(input.split(pattern).toSeq);
  }

  def main(args: Array[String]): Unit = {
    val fileName = "lotr.txt"
    val fileNameStopWords = "./stopwords_en.txt"

    val fileStopWords = Source.fromFile(fileNameStopWords, "UTF-8")
    val stopWords = fileStopWords.mkString.split("\\s+")
    fileStopWords.close

    val file = Source.fromFile(fileName, "UTF-8")
    val fileContent = file.mkString

    getChapters(fileContent).foreach { tuple =>
      writeFile("chapters/" + tuple._1 + ".txt", tuple._2.split("\n"));
    }

    val reduced = countWords(fileContent, stopWords);

    val sorted = reduced.sortWith((a, b) => a._2 > b._2).take(1000)
    file.close

    writeFile("wordcloud.csv", sorted.map(x => x._2 + "," + x._1))
  }
}
