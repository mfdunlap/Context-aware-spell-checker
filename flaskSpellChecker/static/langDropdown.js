$(document).ready(function () {
    function setWebTextLang() {
        var webTextBtn = $("#webTextLang");
        var webTextItems = $("#webTextOptions");

        $(webTextItems).click(function () {
            var webTextLang = $(this).attr("webTextLang")
            console.log(webTextLang)
            hideMenu(webTextItems);
        });
    }

    function getWebTextLang() {

    }

    function setSpellCheckLang() {
        var spellCheckBtn = $("#spellCheckLang");
    }

    function getSpellCheckLang() {

    }

    function hideDropdown(dropdown) {
        $(dropdown).hide(100);
    }
});