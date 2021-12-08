import sys
import csv
import ast
import json
from configparser import ConfigParser

class Dictionary:
    def __init__(self, language, numWords=100000):
        self._language = language
        self.numWord = numWords
        self._wordFreqList, self._prevFreqList, self._nextFreqList  = self.__createFreqList(language, numWords)
        

    def __createFreqList(self, language, numEntries):
        print("Creating", language, "dictionary...")
        csv.field_size_limit(sys.maxsize)
        
        configFile = ConfigParser()
        configFile.read("flaskSpellChecker/config.ini")
        
        root = configFile['DEFAULT']['root']
        wordFreqFile = root + '/' + "freqListData/" + language + "/" + language + "FreqList.json"
        prevWordFreqFile = root + '/' + "freqListData/" + language + "/" + language + "PrevFreqList.json"
        nextWordFreqFile = root + '/' + "freqListData/" + language + "/" + language + "NextFreqList.json"
        
        wordDict = self.__convertJsonToDict(wordFreqFile)
        #wordDict = self.__makeFrequencyDict(wordFreqFile, numEntries)

        prevWordDict = self.__convertJsonToDict(prevWordFreqFile)
        #prevWordDict = self.__makeSurroundingWordsDict(prevWordFreqFile, numEntries)

        nextWordDict = self.__convertJsonToDict(nextWordFreqFile)
        #nextWordDict = self.__makeSurroundingWordsDict(nextWordFreqFile, numEntries)

        print("Dictionary created.")
        return wordDict, prevWordDict, nextWordDict


    def __convertJsonToDict(self, jsonFile):
        newDict = dict()

        with open(jsonFile) as file:
            newDict = json.load(file)

        return newDict



    def __makeFrequencyDict(self, wordFile, numEntries):
        configFile = ConfigParser()
        configFile.read("flaskSpellChecker/config.ini")
        
        root = configFile['DEFAULT']['root']
        wordDictLocation = root + '/' + "freqListData/" + self._language + "/" + self._language + "FreqList.json"

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

        with open(wordDictLocation, "w") as outfile:
            json.dump(freqDict, outfile)

    def __makeSurroundingWordsDict(self, wordFile, numEntries):

        configFile = ConfigParser()
        configFile.read("flaskSpellChecker/config.ini")
        
        root = configFile['DEFAULT']['root']
        wordDictLocation = root + '/' + "freqListData/" + self._language + "/" + self._language + "NextFreqList.json"

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

        with open(wordDictLocation, "w") as outfile:
            json.dump(freqDict, outfile)

        return freqDict

    def getWordFreq(self):
        return self._wordFreqList

    def getNextWordFreq(self):
        return self._nextFreqList

    def getPrevWordFreq(self):
        return self._prevFreqList