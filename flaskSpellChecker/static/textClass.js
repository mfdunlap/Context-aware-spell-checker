// class for text management
class textClass {

    #text;
    #words;
    #htmlText;
    #misspelledWords;
    #textIndexes;
    #textTokens;
  
    constructor(text = "", words = [], textIndexes = [], htmlText = "", textTokens = new Object(), misspelledWords = []) {
      this.#text = text
      this.#textIndexes = textIndexes
      this.#htmlText = htmlText
      this.#misspelledWords = misspelledWords
      this.#textTokens = textTokens
      this.#words = words
    }
  
    getPlainText() {
      return this.#text;
    }
  
    updateText(text) {
      // Update text variable and fill the words' object array with the text area words
  
      this.#text = text;
      console.log("text input", text)
      console.log("text split", text.split(/\s/))
  
      text.split(/\s/).forEach((word,i) => {
        //if(!(this.#words.some(obj => obj.index==i && obj.word==word))){
          if (word != /s/){
          this.#words[i] = {
            'word': word,
            'index': i,
            'html': word,
            }
          console.log("Insert word "+word+" with index "+i)
          }
      //  }
      })
    }
  
    removeUnderlines(){
      // Remove all the underlines from the text
      this.#words.forEach(obj =>{
        obj.html = obj.word
      })
      console.log("prova")
      this.printWordList()
      this.replaceHtmlText()
    }
  
    cleanWords(){
      // Reset the words array
      this.#words = []
    }
  
    getHtmlText(){
      // Build the html text from the word array
      var wordArray = this.#words
      let htmlText = []
      wordArray.forEach(obj => {
        htmlText.push(obj.html)
      })
      return htmlText
    }
  
    updateHtmlText(newHtmlText) {
      // Store the htmlText in the private variable
      this.#htmlText = newHtmlText;
    }
  
    getMisspelledWords() {
      return this.#misspelledWords;
    }
  
    getWordByIndex(index){
      return this.#textIndexes[index]
    }
  
    printWord(string){
      // Print a specific word object given the word string
      console.log("Word:", this.#words.find(obj => obj.word==string))
    }
  
    printWordList(){
      // Print the entire current words array
      this.#words.forEach(word => {
        console.log("Object: ",word['word'] + "\n" + word['index'] + "\n" + word['html'])
        })
    }

    pushWord(word, index, html){
      this.#words.push({
        "word": word,
        "index": index,
        "html": html
      })
    }
  
    updateMisspelledWords(misspelledWordsList) {
      // Replace the html field of the misspelled word objects
  
      this.#misspelledWords = misspelledWordsList;
      var misspelledArr = this.#misspelledWords
  
      if (misspelledWordsList.length>0){
        misspelledArr.forEach((misspelling,i) => {
          if (typeof misspelling == 'string'){
            var htmlToken = '<span style="text-decoration: underline 2px red;">' + misspelling + '</span>'
            var objIndex = this.#words.findIndex(word => word.index == misspelledArr[i+1][0])
            //console.log("Adding html to word ["+misspelling +" "+ objIndex+"] with index=", misspelledArr[i+1][0])
            //console.log("objects:",this.printWordList())
            this.#words[objIndex].html = htmlToken
            this.printWord(this.#words[objIndex].word)
          }
        })
      }
    }
  
    replaceHtmlText(){
      // Put the html text into the web text area, joining the words array html fields
      document.getElementById("textArea").innerHTML = textSingleton.getHtmlText().join("&nbsp")
    }
  
    getIndexbyWord(word){
      for(var i=0; i<=this.#textIndexes.length; i++){
        if (this.#textIndexes[i].match(word)){
          return i;
        }
      }
      return -1;
    }
  
    replaceMisspelledWithCorrection(newToken, index){
      // Modify a word object within the word array when a correction is selected
      var wordIndex = this.#words.findIndex(obj=>obj.index==index)
      this.#words[wordIndex].word = newToken
      this.#words[wordIndex].html = newToken
    }
  };

// global text instance
var textSingleton = new textClass()