import configparser
from spellchecker import SpellChecker
import string
import re
from flaskSpellChecker.dictionary import Dictionary

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


def spellCheckText(dictionary, text):
    misspellings = dict()
    wordIndex = dict()
    wordlist = text.split()
    numWords = len(wordlist)

    for i in range(numWords):
        
        word = wordlist[i]
        prevWord = ""
        nextWord = ""

        if 0 <= i-1 < numWords:
            prevWord = wordlist[i-1]

        if 0 <= i+1 < numWords:
            nextWord = wordlist[i+1]

        contextedWord = (" ".join([prevWord, word, nextWord])).strip()

        if not contextedWord in misspellings:
            corrections = spellCheckWord(dictionary, word, prevWord, nextWord)

            if corrections:
                misspellings[contextedWord] = corrections
                wordIndex[contextedWord] = [i]
        else:
            wordIndex[contextedWord].append(i)
    
    return misspellings, wordIndex


def spellCheckWord(dictionary, word, prevWord="", nextWord=""):
    """
        This function return a ranked lists of potentional corrections for a word with or without context.
        
        Arguments:
            - dictionary: a frequency dictionary of words to check the spelling of word
            - word: the word to be spell checked
            - prevWord: the word before word (optional)
            - nextWord: the word after word (optional)
            
        Returns:
            - correctionsList: a ranked list of possible corrections for word if word is misspelled
            - correctionsList: a list containing the only the value -1 for misspelled words with no found corrections
            - correctionsList: an empty list if word is correctly spelled    
    """

    correctionsList = list()
    freqDict = dictionary.getWordFreq()
    lenWord = len(word)

    # Determine appropriate edit distance from length of the word
    if lenWord < 5:
        editDist = 1
    else:
        editDist = 2

    # Check if word is numerical outside of punctuation:
    wordWithoutPunct = re.sub(r'[^\w\s]','', word)
    wordIsNumBased = wordWithoutPunct.isdigit()

    # Check if word is only punctuation:
    punct = string.punctuation
    wordIsPunct = all(c in punct for c in word)

    # Check if word is correctly spelled:
    word = word.strip(punct)
    wordIsValid = word in freqDict or word.lower() in freqDict

    # Return empty list if valid term:
    if wordIsNumBased or wordIsPunct or wordIsValid:
        return correctionsList

    correctionsList = getCorrections(dictionary, word, prevWord, nextWord, editDist)

    return correctionsList


def getCorrections(dictionary, word, prevWord="", nextWord="", editDist=1):
    alphabet = 'abcdefghilmnoprstuáéíóú-'
    freqDict = dictionary.getWordFreq()
    noPossibleCorrections = [-1]

    # Get potential corrections:
    splitMisspell = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splitMisspell if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splitMisspell if len(b)>1]
    replaces = [a + c + b[1:] for a, b in splitMisspell for c in alphabet if b]
    inserts = [a + c + b for a, b in splitMisspell for c in alphabet]
    splits = [(" ".join([a,b])).strip() for a,b in splitMisspell]

    suggestions = list(set(deletes + transposes + replaces + inserts + splits))

    if editDist > 1:
        newSuggestions = list()
        for item in suggestions:
            recursiveSuggest = getCorrections(dictionary, item, prevWord, nextWord, editDist=editDist-1)
            if recursiveSuggest != noPossibleCorrections:
                newSuggestions.extend(recursiveSuggest)

        suggestions.extend(newSuggestions)
        suggestions = list(set(suggestions))

    possibleCorrections = [suggestion for suggestion in suggestions if suggestion in freqDict]

    if not possibleCorrections:
        return noPossibleCorrections       

    rankedMisspellings = rankCorrections(dictionary, possibleCorrections, prevWord, nextWord)
    return rankedMisspellings


def rankCorrections(dictionary, possibilities, prevWord="", nextWord=""):
    rankedCorrectionsDict = dict()

    wordDict = dictionary.getWordFreq()
    prevWordDict = dictionary.getPrevWordFreq()
    nextWordDict = dictionary.getNextWordFreq()

    totalWords = sum(wordDict.values())

    for suggestion in possibilities:
        firstSuggest = suggestion
        secondSuggest = suggestion

        if ' ' in suggestion:
            splitSuggestion = suggestion.split()
            firstSuggest = splitSuggestion[0]
            secondSuggest = splitSuggestion[1]

        # Calculate probability that word is used:
        if firstSuggest == secondSuggest:
            probWord = wordDict[suggestion] / totalWords
        else:
            if secondSuggest in nextWordDict[firstSuggest]:
                totalCombo = sum(nextWordDict[firstSuggest].values())
                probWord = nextWordDict[firstSuggest][secondSuggest] / totalCombo
            else:
                probWord = 0

        # Calculate probability that prevWord is the word before the suggestion:
        if prevWord and prevWord in prevWordDict[firstSuggest]:
            totalPrevWords = sum(prevWordDict[firstSuggest].values())
            probPrevWord = prevWordDict[firstSuggest][prevWord] / totalPrevWords
        else:
            probPrevWord = 0

        # Calculate probability that nextWord is the word after the suggestion
        if nextWord and nextWord in nextWordDict[secondSuggest]:
            totalNextWords = sum(nextWordDict[secondSuggest].values())
            probNextWord = nextWordDict[secondSuggest][nextWord] / totalNextWords
        else:
            probNextWord = 0

        # Calculate weighted estimate that suggestion is the correct replacement
        weightedEst = 0.6*probWord + 0.2*probPrevWord + 0.2*probNextWord
        rankedCorrectionsDict[suggestion] = weightedEst

    # Rank suggestion by weighted estimate
    rankedCorrections = sorted(rankedCorrectionsDict, key=rankedCorrectionsDict.get, reverse=True)

    return rankedCorrections


if __name__ == "__main__":
    text = ""
    ga = Dictionary('ga')

    #    irishDict, prevDict, nextDict = generateIrishDictionary()
    #    print("Word: an")
    #    print("Next Words:", nextDict["an"])

    #text = "Sin, sin. SIn: SIN? xin, xin. XIn; XIN!"

    #text = "a xin an. Iúdá ajus! ró luath ag. ró l-uat-h ag"

    #misspellings = spellCheckWord(ga, "xin")
    #print("Xin Corrections:", misspellings)

    #misspellings = spellCheckWord(ga, "xin", "a", "an")
    #print("Xin Corrections:", misspellings)

    #misspellings = spellCheckWord(ga, "xin", prevWord="a")
    #print("Xin Corrections:", misspellings)

    #misspellings = spellCheckWord(ga, "xin", nextWord="an")
    #print("Xin Corrections:", misspellings)

    #misspellings, index = spellCheckText(ga, text)
    #print("Mispellings:", misspellings)
    #print("Indices:", index)

    while (text != "exit"):
        text = str(input("Enter text to spell check (Irish): "))
        misppellings, indicies = spellCheckText(ga, text)
        print("Misspellings:", misppellings)
        print("Indices of Mispellings:", indicies)
        print()
