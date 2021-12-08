function setWebTextLang(lang, langID) {
    console.log("Button Clicked", lang)
    var elementID = '#webTextLang';
    $.ajax({
        type: "POST",
        url: "/set_webtext_language",
        cache: false,
        dataType: "json",
        data: {
          'langCode': lang,
        },
    
        success: function (confirmation) {
            console.log(confirmation);
            sessionStorage.setItem("reloading", "true");
            sessionStorage.setItem("elementID", elementID);
            sessionStorage.setItem("langID", langID);
            document.location.reload();
        },
    });
    
}

window.onload = function() {
    var reloading = sessionStorage.getItem("reloading"),
        elementID = sessionStorage.getItem("elementID"),
        langID = sessionStorage.getItem("langID");

    if (reloading) {
        sessionStorage.removeItem("reloading");
        langTranslation = document.getElementById(langID).innerHTML;
        console.log(langTranslation)
        changeText(elementID, langTranslation);
        sessionStorage.removeItem("elementID"),
        sessionStorage.removeItem("langID");
    }
}

function changeText(elementID, newHTML) {
    $(elementID).empty().append(newHTML)
}