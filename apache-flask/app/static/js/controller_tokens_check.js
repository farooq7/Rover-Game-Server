var token_check = false;
var win = false;

var reset_win = function() {
    win = false;
};

var enable_token_check = function() {
    token_check = true;
};

var disable_token_check = function() {
    token_check = false;
};

var check_winners = function() {
    if (!token_check || win) {
        return;
    }
    if (window.localStorage.getItem("blue_ip") != "") {
        check_token_count(window.localStorage.getItem("blue_ip"), "blue");
    }
    if (window.localStorage.getItem("red_ip") != "") {
        check_token_count(window.localStorage.getItem("red_ip"), "red");
    }
}

var check_token_count = function(target, color) {
    var r = new XMLHttpRequest();
    r.open("POST", "/api/get_tokens");
    r.send();
    r.onload = function() {
        if (r.status != 200) {
            console.log("Unable to get tokens.");
            return;
        }
        var tokens = JSON.parse(r.responseText);
        var token_count = calc_token_count(target, color, tokens);
        check_win(target, token_count);
    };
};

var calc_token_count = function(target, color, tokens) {
    var token_count = 0;
    for (var i = 0; i < tokens.length; i++) {
        var token = tokens[i];
        if (token['color'] == color && token['collected'] == true) {
            token_count = token_count + 1;
        }
    }
    console.log(target, color, token_count);
    return token_count;
};

var check_win = function(target, token_count) {
    if (token_count >= 5) {
        win = true;
        show_announcement(translate_ip(target) + " has collected all 5 tokens!");
        setTimeout(hide_announcement, 3000);
    }
};

window.setInterval(check_winners, 1000);
