var show_shroud = function() {
    document.getElementById("shroud").style.display = "block";
};

var hide_shroud = function() {
    document.getElementById("shroud").style.display = "none";
};

var show_setup_menu = function() {
    show_shroud();
    document.getElementById("setup-menu").style.display = "block";
};

var hide_setup_menu = function() {
    hide_shroud();
    document.getElementById("setup-menu").style.display = "none";
};

var show_announcement = function(s) {
    document.getElementById("announcement").innerHTML = s;
    show_shroud();
    document.getElementById("announcement").style.display = "block";
};

var hide_announcement = function() {
    hide_shroud();
    document.getElementById("announcement").style.display = "none";
};

document.getElementById("announcement").onclick = function() {
    hide_announcement();
};

window.localStorage.setItem("team", "spectator");
window.localStorage.setItem("blue-ip", "");
window.localStorage.setItem("red-ip", "");