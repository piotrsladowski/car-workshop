    function validateFormNewJob() {
        var x = document.forms["rForm"]["rname"].value;
        var format = /[ `!@#$%^&*()+=\[\]{};':"\\|,.<>\/?~]/;
        if (x == "spadaj") {
            var audio = new Audio("static/audio/DIA_ADDON_BL_BDT_13_GOLD_13_03.OPUS");
            audio.play();
            return false;
        }
        if (format.test(x)) {
            var amarel = getCookie("amarel");
            if (amarel != "") {
                if (amarel == "1") {
                    document.cookie = "amarel=2";
                    var audio = new Audio("static/audio/INFO_GRD_6_DIELAGE_06_01.OPUS");
                    audio.play();
                } else if (amarel == "2") {
                    document.cookie = "amarel=3";
                    var audio = new Audio("static/audio/DIA_SEKOB_HALLO_01_00.OPUS");
                    audio.play();
                } else if (amarel == "3") {
                    document.cookie = "amarel=4";
                    var audio = new Audio("static/audio/DIA_RUMBOLD_PREPERM_10_01.OPUS");
                    audio.play();
                } else if (amarel == "4") {
                    document.cookie = "amarel=5";
                    var audio = new Audio("static/audio/INFO_Player_PC_Hero_BPANKRATZ3249_Polish.ogg");
                    audio.play();
                } else if (amarel == "5") {
                    document.cookie = "amarel=6";
                    var audio = new Audio("static/audio/DIA_RAOUL_TROLL_RECHNUNG_B_RAOUL_BLAME_01_00.OPUS");
                    audio.play();
                    setTimeout(function (){
                    window.location.href = "https://g02.labagh.pl/gameOver";
                    }, 7000);
                } else {
                    var audio = new Audio("static/audio/SVM_8_SMALLTALK18.OPUS");
                    audio.play();
                }
            } else {
                document.cookie = "amarel=1";
                var audio = new Audio("static/audio/INFO_BLOODWYN_DIE_08_07.OPUS");
                audio.play();
            }

            return false;
        }
    }
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }