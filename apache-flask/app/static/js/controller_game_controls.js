document.getElementById("start-game-button").onclick = function () {
    enable_notifications();
    enable_display();
    enable_token_check();
    enable_check_direction();
};

document.getElementById("stop-game-button").onclick = function () {
    disable_notifications();
    disable_display();
    disable_token_check();
    disable_check_direction();
    document.getElementById('blue-img').style.display = "none";
    document.getElementById('red-img').style.display = "none";
};

document.getElementById("setup-game-button").onclick = function () {
    show_setup_menu();
};

document.getElementById("reset-game-button").onclick = function () {
    document.getElementById('logs-area').innerHTML = "";
    var r = new XMLHttpRequest();
    r.open("POST", "/api/reset");
    r.send();
    log_date(new Date(), "Game has been reset.");
    reset_win();
};

document.getElementById("calibrate-game-button").onclick = function () {
    if (get_target() == "") {
        return;
    }
    var r = new XMLHttpRequest();
    r.open("POST", "/api/calibrate/" + get_target());
    r.send();
    log_date(new Date(), "Sending calibrate command.");
};

var get_target = function() {
    if (window.localStorage.getItem("team") == "blue") {
        return window.localStorage.getItem("blue_ip")
    }
    else if (window.localStorage.getItem("team") == "red") {
        return window.localStorage.getItem("red_ip")
    }
    else {
        return "";
    }
};

var save_game_info = function (blue_ip, red_ip, team) {
    window.localStorage.setItem("blue_ip", blue_ip);
    window.localStorage.setItem("red_ip", red_ip);
    window.localStorage.setItem("team", team);
};

document.getElementById("setup-menu-submit-button").onclick = function (e) {
    var team = "";
    var team_input_radios = document.getElementsByName("team-input");
    for (var i = 0; i < team_input_radios.length; i++) {
        if (team_input_radios[i].checked) {
            team = team_input_radios[i].value;
            break;
        }
    }
    set_title_bar_color(team);
    if (team == "spectator") reset_color();
    var blue_ip = document.getElementById("blue-ip-input").value;
    var red_ip = document.getElementById("red-ip-input").value;
    save_game_info(blue_ip, red_ip, team);
    hide_setup_menu();
};

var set_title_bar_color = function(team) {
    if (team == "blue") {
        document.getElementById("title-bar").style.backgroundColor = "rgba(72, 96, 255, 1)";
    }
    else if (team == "red") {
        document.getElementById("title-bar").style.backgroundColor = "rgba(232, 48, 48, 1)";
    }
    else if (team == "spectator") {
        document.getElementById("title-bar").style.backgroundColor = "rgba(48, 48, 48, 1)";
    }
}
