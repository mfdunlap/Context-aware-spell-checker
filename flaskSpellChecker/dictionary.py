import sys
import csv
import ast

class Dictionary:
    def __init__(self, language, numWords=10000):
        self._language = language
        self.numWord = numWords
        self._wordFreqList, self._prevFreqList, self._nextFreqList  = self.__createFreqList(language, numWords)
        

    def __createFreqList(self, language, numEntries):
        print("Creating dictionary...")
        csv.field_size_limit(sys.maxsize)

        wordFreqFile = "freqListData/" + language + "/" + language + "FreqList.csv"
        prevWordFreqFile = "freqListData/" + language + "/" + language + "PrevFreqList.csv"
        nextWordFreqFile = "freqListData/" + language + "/" + language + "NextFreqList.csv"
        
        wordDict = self.__makeFrequencyDict(wordFreqFile, numEntries)
        prevWordDict = self.__makeSurroundingWordsDict(prevWordFreqFile, numEntries)
        nextWordDict = self.__makeSurroundingWordsDict(nextWordFreqFile, numEntries)

        print("Dictionary created.")
        return wordDict, prevWordDict, nextWordDict

    def __makeFrequencyDict(self, wordFile, numEntries):
        with open(wordFile, newline='', encoding='utf-8') as file:
            csvReader = csv.reader(file)
            freqDict = dict()
            
            for row in csvReader:
                freqRank = int(row[0])
                word = row[1]
                frequency = int(row[2])

                if freqRank > numEntries:
                    break

                freqDict[word] = frequency
        
        return freqDict

    def __makeSurroundingWordsDict(self, wordFile, numEntries):
        with open(wordFile, newline='', encoding='utf-8') as file:
            csvReader = csv.reader(file)
            freqDict = dict()
            
            for row in csvReader:
                freqRank = int(row[0])
                word = row[1]
                surroundingWords = ast.literal_eval(row[2])

                if freqRank > numEntries:
                    break

                freqDict[word] = surroundingWords

        return freqDict

    def getWordFreq(self):
        return self._wordFreqList

    def getNextWordFreq(self):
        return self._nextFreqList

    def getPrevWordFreq(self):
        return self._prevFreqList