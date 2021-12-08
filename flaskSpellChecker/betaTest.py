from flaskSpellChecker import utils
import csv

if __name__ == "__main__":    
    #dirRoot = 'flaskSpellChecker/testFiles/testset/'
    #filePath = dirRoot + 'input.txt'
    #answerPath = dirRoot + 'alphaTest_answers.tsv'
    #solutionsPath = dirRoot + 'corrections500.tsv'
    #lang = utils.ga
    #numTests = 10000

    #dirRoot = 'flaskSpellChecker/testFiles/input-test/'
    #filePath = dirRoot + 'input-test.txt'
    #answerPath = dirRoot + 'alphaTest_answersFINAL.tsv'
    #lang = utils.ga
    #numTests = 59000

    dirRoot = 'flaskSpellChecker/testFiles/en-input/'
    filePath = dirRoot + 'en-input.txt'
    answerPath = dirRoot + 'enTest_answersFINAL.tsv'
    lang = utils.en
    numTests = 290

    # Generate answers:
    with open(filePath, newline='\n', encoding='utf-8') as file:
        tokenList = file.readlines()
        answerList = list()
        numWords = len(tokenList)
        counter = 0

        for i in range(numWords):
            word = tokenList[i].strip()
            prevWord = ""
            nextWord = ""

            if 0 <= i-1 < numWords:
                prevWord = tokenList[i-1].strip()

            if 0 <= i+1 < numWords:
                nextWord = tokenList[i+1].strip()

            corrections = utils.spellCheckWord(lang, word, prevWord, nextWord)

            if not corrections:
                answer = word
            elif corrections[0] == -1:
                answer = "Misspelled but no correction found"
            else:
                answer = corrections[0]

            answerList.append(answer)
            counter += 1
            
            if(i%1000 == 0):
                print(str((i%1000)*10) + "% Complete")

        print("Same number of answers and tokens:", counter == numWords)
        
        with open(answerPath, mode='wt', encoding='utf-8', newline='') as writeFile:
            tsv_writer = csv.writer(writeFile, delimiter='\t')
            for i in range(numWords):
                tsv_writer.writerow([tokenList[i].strip(), answerList[i]])
            
            print(answerPath, "created.")

    # Check answers (testset only):
    """
    ourAnswerKey = list()
    correctAnswers = 0
    index = 1

    with open(answerPath, newline='', encoding='utf-8') as ourAnswers:
        answerReader = csv.reader(ourAnswers, delimiter="\t")
        for row in answerReader:
            if 0 <= index < len(row):
                ourAnswerKey.append(row[index].strip())

    with open(solutionsPath, newline='', encoding='utf-8') as solutionKey:
        solutionReader = csv.reader(solutionKey, delimiter="\t")
        rowNum = 0
        for row in solutionReader:
            if 0 <= index < len(row):
                if ourAnswerKey[rowNum] == row[index].strip():
                    correctAnswers += 1
                else:
                    #print("ERROR(" + str(j+1) + ": Answer", ourAnswerKey[j], "should be", trueSolutionKey[j])
                    pass
                rowNum += 1

    totalCorrections = len(ourAnswerKey)    
    print("Percent Correct:", 100 * correctAnswers / totalCorrections)
    """
    