import configparser
from spellchecker import SpellChecker
from textblob import TextBlob
import re
from flaskSpellChecker import dictionary
from dictionary import Dictionary

def simpleChecker(text):
    
    # Read file
    #print("Original Text:\n", str(text))
    # Remove punctuation using regex
    s = re.sub(r'[^\w\s]','', text)
    #print("Text without punctuations:\n",s)
    wordlist=s.split()
    spell = SpellChecker()
    misspelled = list(spell.unknown(wordlist))
    idxDict = dict()
    for index, word in enumerate(wordlist):
        if word in misspelled:
            idxDict[word] = index

    #print("DEBUG: ", idxDict)
    #print("Possible list of misspelled words in the original text:\n",misspelled)

    # Use pyspellchecker to correct the word and list candidates
    candidates = dict()
    for word in misspelled:
        # Get the one `most likely` answer
        #print("Correct word:",spell.correction(word))
        # Get a list of `likely` options
        #print("Candidate words:",spell.candidates(word))
        candidates[word] = spell.candidates(word)
    
    #print(candidates)
    return candidates, misspelled, idxDict
        
def getResultsPath():
    configFile = configparser.ConfigParser()
    configFile.read("flaskSpellChecker/config.ini")
    return configFile['DEFAULT']['json_path']

def checkSpelling(text, dictionary):
    misspellings = dict()
    wordIndex = dict()
    emptySlot = "WordDoesntExist"

    gaDict = dictionary.getWordFreqList()
    
    p = re.compile(r"(\b[-']\b)|[\W_]")
    wordOnlyText = p.sub(lambda m: (m.group(1) if m.group(1) else " "), text)
    wordlist = wordOnlyText.split()

    for i, word in enumerate(wordlist):
        wordContext = ["WordDoesntExist", word, "WordDoesntExist"]

        if 0 <= i-1 < len(wordlist):
            wordContext[0] = wordlist[i-1]

        if 0 <= i+1 < len(wordlist):
            wordContext[2] = wordlist[i+1]

        wordContextString = " ".join(wordContext)

        if not (wordContext[1] in gaDict or wordContext[1].lower() in gaDict):
            
            if not wordContextString in misspellings:
                misspellings[wordContextString] = dict()

                for j in range(len(wordContext)):
                    if wordContext[j] == emptySlot:
                        wordContext[j] = ""
                wordContextString = (" ".join(wordContext)).strip()
                wordIndex[wordContextString] = list()
            
            wordIndex[wordContextString].append(i)

    corrections = getCorrections(misspellings, dictionary)

    return corrections, wordIndex


def getCorrections(misspellingsDict, dictionary):
    alphabet = 'abcdefghilmnoprstuáéíóú-'
    dictionaryWords = dictionary.getWordFreqList()


    for key in misspellingsDict.keys():
        splitContext = key.split()
        misspell = splitContext[1]

        splitMisspell = [(misspell[:i], misspell[i:]) for i in range(len(misspell) + 1)]
        deletes = [a + b[1:] for a, b in splitMisspell if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splitMisspell if len(b)>1]
        replaces = [a + c + b[1:] for a, b in splitMisspell for c in alphabet if b]
        inserts = [a + c + b for a, b in splitMisspell for c in alphabet]
        
        suggestions = list(set(deletes + transposes + replaces + inserts))
        misspellingsDict[key] = [suggestion for suggestion in suggestions if suggestion in dictionaryWords]

        for a,b in splitMisspell:
            if a in dictionaryWords and b in dictionaryWords:
                misspellingsDict[key].append(a + " " + b)

    rankedMisspellingsDict = rankGaCorrections(misspellingsDict, dictionary)
    return rankedMisspellingsDict


def rankGaCorrections(correctionsDict, dictionary):
    rankedCorrectionsDict = dict()

    wordDict = dictionary.getWordFreqList()
    nextWordDict = dictionary.getNextWordFreqList()
    prevWordDict = dictionary.getPrevWordFreqList()

    totalWords = sum(wordDict.values())

    for key, value in correctionsDict.items():
        correctionranking = dict()
        emptySlot = "WordDoesntExist"
        splitContext = key.split()

        if splitContext[0] != emptySlot:
            prevWord = splitContext[0]
        else:
            prevWord = ""

        misspell = splitContext[1]

        if splitContext[2] != emptySlot:
            nextWord = splitContext[2]
        else:
            nextWord = ""

        for suggestion in value:

            if not (' ' in suggestion):
                probWord = wordDict[suggestion] / totalWords

                if nextWord in nextWordDict[suggestion]:
                    totalNextWords = sum(nextWordDict[suggestion].values())
                    probNextWord = nextWordDict[suggestion][nextWord] / totalNextWords
                else:
                    probNextWord = 0
            
                if prevWord in prevWordDict[suggestion]:
                    totalPrevWords = sum(prevWordDict[suggestion].values())
                    probPrevWord = prevWordDict[suggestion][prevWord] / totalPrevWords
                else:
                    probPrevWord = 0

            else:
                suggestWords = suggestion.split()
                suggest1 = suggestWords[0]
                suggest2 = suggestWords[1]
                
                if suggest2 in nextWordDict[suggest1]:
                    totalNextWords = sum(nextWordDict[suggest1].values())
                    probWord = nextWordDict[suggest1][suggest2] / totalNextWords
                else:
                    probWord = 0

                if nextWord in nextWordDict[suggest2]:
                    totalNextWords = sum(nextWordDict[suggest2].values())
                    probNextWord = nextWordDict[suggest2][nextWord] / totalNextWords
                else:
                    probNextWord = 0

                if prevWord in prevWordDict[suggest1]:
                    totalPrevWords = sum(prevWordDict[suggest1].values())
                    probPrevWord = prevWordDict[suggest1][prevWord] / totalPrevWords
                else:
                    probPrevWord = 0
            
            probability = 0.6*probWord + 0.2*probPrevWord + 0.2*probNextWord
            correctionranking[suggestion] = probability
        print(correctionranking)
        rankedCorrections = sorted(correctionranking, key=correctionranking.get, reverse=True)
        misspellContext = (" ".join([prevWord, misspell, nextWord])).strip()
        rankedCorrectionsDict[misspellContext] = rankedCorrections

    return rankedCorrectionsDict


if __name__ == "__main__":
    ga = Dictionary('ga')

    #    irishDict, prevDict, nextDict = generateIrishDictionary()
    #    print("Word: an")
    #    print("Next Words:", nextDict["an"])

    #text = "Sin, sin. SIn: SIN? xin, xin. XIn; XIN!"
    text = "a xin an. Iúdá ajus! ró luath ag"
    misspellings, index = checkSpelling(text, ga)
    print("Mispellings:", misspellings)
    print("Indices:", index)
