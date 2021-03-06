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
    val reduced = grouped.mapValues(x => x.length).toSeq
    val sorted = reduced.sortWith((a, b) => a._2 > b._2).take(100)

    return sorted;
  }

  def getChapters(input: String): Seq[(String, String)] = {
    val pattern = "####-\\s*\\n*(Chapter \\d+\\.?(\\s[\\w-]+)*)"
    val re = pattern.r;
    val chapters = re.findAllIn(input).matchData.map(m => m.group(1)).toSeq
    return chapters.zip(input.split(pattern).toSeq);
  }

  def addTermFrequencies(
      wordCount: Seq[(String, Int)],
      chapterStats: Seq[(String, Seq[(String, Int)])]
  ): Seq[(String, Int, Double)] = {
    val sumOfTerms = wordCount.map(word => word._2).sum;
    val numberOfChapters = chapterStats.length;

    val termFrequencies =
      wordCount.map(word => {
        val tf = word._2.toFloat / sumOfTerms;
        val idf = math.log(
          numberOfChapters.toFloat / (chapterStats.count(chapter =>
            chapter._2.map(stat => stat._1).contains(word._1)
          ) + 1)
        );

        val result = (
          word._1,
          word._2,
          tf * idf
        );

        result;
      });

    termFrequencies;
  }

  def findChaptersHighestTFIDFWord(
      word: String,
      chapters: Seq[(String, Seq[(String, Int, Double)])]
  ): Seq[String] = {
    val matchingChapters =
      chapters
        .filter(chapter => chapter._2.map(w => w._1).contains(word))
        .map(chapter => (chapter._1, chapter._2.find(w => w._1 == word).get))
        .sortBy(item => item._2._3)
    return matchingChapters.map(chapt => chapt._1);
  }

  def main(args: Array[String]): Unit = {
    val fileName = "lotr.txt"
    val fileNameStopWords = "./stopwords_en.txt"

    val fileStopWords = Source.fromFile(fileNameStopWords, "UTF-8")
    val stopWords = fileStopWords.mkString.split("\\s+")
    fileStopWords.close

    val file = Source.fromFile(fileName, "UTF-8")
    val fileContent = file.mkString
    file.close

    val chapters = getChapters(fileContent)

    val chapterStats = chapters.map(chapter => {
      val chapterName = chapter._1
      val chapterContent = chapter._2

      // writeFile("chapters/" + chapterName + ".txt", chapterContent.split("\n"));

      val wordCount = countWords(chapterContent, stopWords);

      (chapterName, wordCount)
    })

    val chapterStats2 = chapterStats.map(cs => {
      val wordCount = cs._2;
      (cs._1, addTermFrequencies(wordCount, chapterStats));
    })

    val sorted = chapterStats2.map(cs =>
      (cs._1, cs._2.sortWith((a, b) => a._3 > b._3).take(100))
    );

    val highestTFIDFWordsPerChapter =
      sorted.map(stats => (stats._1, stats._2.take(20).map(word => word._1)))

    highestTFIDFWordsPerChapter.foreach { item =>
      println(item._1 + "\n\t" + item._2.mkString("\n\t"))
    }

    println("Search word: ")
    val searchWord = scala.io.StdIn.readLine()
    findChaptersHighestTFIDFWord(searchWord, sorted).foreach { println }

    sorted.foreach(chapter => {
      val chapterName = chapter._1;
      val stats = chapter._2;
      writeFile(
        "wordclouds/" + chapterName + ".csv",
        stats.map(x => math.ceil(x._3 * 1000).toInt + "," + x._1)
      )
    })

    val wholeBookWords = sorted
      .flatMap(chapter => chapter._2)
      .groupBy(word => word._1)
      .mapValues(words => (words.map(w => w._3).sum * 1000).toInt)
      .toSeq

    writeFile(
      "wordcloud.csv",
      wholeBookWords.sortBy(x => -x._2).map(x => x._2 + "," + x._1)
    )
  }
}
