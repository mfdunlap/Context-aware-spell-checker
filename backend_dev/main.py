from spellchecker import SpellChecker
import spellchecker
from textblob import TextBlob
import re

import contextualSpellCheck
import spacy
import en_core_web_sm

# Main
def simpleChecker():
    
    # Read file
    file1="./backend-features/words.txt"
    with open(file1,"r+") as filehandle:
        filecontent=filehandle.read()
        print("Original Text:\n", str(filecontent))
        # Convert the text into a TextBlob object
        b = TextBlob(filecontent)
        # Textblob correction -> bad
        # print("Corrected text:\n", str(b.correct()))

    # Remove punctuation using regex
    s = re.sub(r'[^\w\s]','',filecontent)
    print("Text without punctuations:\n",s)
    wordlist=s.split()
    spell = SpellChecker()
    misspelled = list(spell.unknown(wordlist))
    print("Possible list of misspelled words in the original text:\n",misspelled)

    # Use pyspellchecker to correct the word and list candidates
    for word in misspelled:
        # Get the one `most likely` answer
        print("Correct word:",spell.correction(word))
        # Get a list of `likely` options
        print("Candidate words:",spell.candidates(word))

def BERTchecker():

    nlp = spacy.load("en_core_web_sm")
    nlp.pipe_names
    ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer']
    # You can pass the optional parameters to the contextualSpellCheck
    # eg. pass max edit distance use config={"max_edit_dist": 3}
    contextualSpellCheck.add_to_pipe(nlp)
    print(nlp.pipe_names)

    # Read file
    file1="./backend-features/words.txt"
    with open(file1,"r+") as filehandle:
            filecontent=filehandle.read()
            print("Original Text:\n", str(filecontent))

    # Training
    doc = nlp(filecontent)
    
    #print(doc._.performed_spellCheck)
    #print(doc._.outcome_spellCheck)

    #print(doc._.contextual_spellCheck)

    #print(doc._.performed_spellCheck)

    print(doc._.suggestions_spellCheck)

    print(doc._.outcome_spellCheck)

    #print(doc._.score_spellCheck)
    print(doc._.score_spellCheck)
    
    #print(doc._.get_suggestion_spellCheck)



simpleChecker()
#BERTchecker()

