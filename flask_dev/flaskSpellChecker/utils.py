from spellchecker import SpellChecker
from textblob import TextBlob
import re

def simpleChecker(text):
    
    # Read file
    #print("Original Text:\n", str(text))
    # Remove punctuation using regex
    s = re.sub(r'[^\w\s]','', text)
    #print("Text without punctuations:\n",s)
    wordlist=s.split()
    spell = SpellChecker()
    misspelled = list(spell.unknown(wordlist))
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
    return candidates, misspelled
        

     