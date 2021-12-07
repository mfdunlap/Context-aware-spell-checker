import csv
import os
import re


def saveToFile(fileName, fileKeys, fileData):
    with open(fileName, mode='w', encoding='utf-8', newline='') as file:
        count = 1
        fileWrite = csv.writer(file, quoting=csv.QUOTE_ALL)

        for key in fileKeys:
            fileWrite.writerow([count, key, fileData[key]])
            count += 1
    print("SUCCESS:", fileName, " Created.")


if __name__ == "__main__":
    dirPath = "freqListData/en/text"
    directory = os.listdir(dirPath)
    wordFreq = dict()
    prevWordFreq = dict()
    nextWordFreq = dict()
    freqFileName = 'englishFreqList.csv'
    prevFreqFileName = 'englishPrevFreqList.csv'
    nextFreqFileName = 'englishNextFreqList.csv'


    for file in directory:
        with open(dirPath + '/' + file, mode='r', encoding='utf-8') as docText:
        
            for line in docText:
                
                p = re.compile(r"(\b[-']\b)|[\W_]")
                line = p.sub(lambda m: (m.group(1) if m.group(1) else " "), line)
                line = line.strip()
                line = line.strip('“')
                line = line.strip('”')
                words = line.split()

                for i, word in enumerate(words):
                    
                    if word in wordFreq:
                        wordFreq[word] += 1
                    else:
                        wordFreq[word] = 1
                        prevWordFreq[word] = dict()
                        nextWordFreq[word] = dict()

                    if i > 1:
                        if words[i-1] in prevWordFreq[word]:
                            prevWordFreq[word][words[i-1]] += 1
                        else:
                            prevWordFreq[word][words[i-1]] = 1
                    
                    if i < len(words)-1:
                        if words[i+1] in nextWordFreq[word]:
                            nextWordFreq[word][words[i+1]] += 1
                        else:
                            nextWordFreq[word][words[i+1]] = 1


    freqSorted = dict()

    sortedKeys = sorted(wordFreq, key=wordFreq.get, reverse=True)
    for sortedKey in sortedKeys:
        freqSorted[sortedKey] = wordFreq[sortedKey]

    
    wordList = freqSorted.keys()
    saveToFile(freqFileName, wordList, freqSorted)
    saveToFile(prevFreqFileName, wordList, prevWordFreq)
    saveToFile(nextFreqFileName, wordList, nextWordFreq)
