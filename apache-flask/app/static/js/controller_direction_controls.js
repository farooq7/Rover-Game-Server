var check_direction_enabled = false;

var enable_check_direction = function() {
    check_direction_enabled = true;  
};

var disable_check_direction = function() {
    check_direction_enabled = false;
};

var check_direction = function() {
    if (check_direction_enabled) {
        var target = get_target();
        if (target == "") return;
        var r = new XMLHttpRequest();
        if (forward) {
            r.open("POST", "/api/control/" + target + "/forward");
        }
        else if (reverse) {
            r.open("POST", "/api/control/" + target + "/reverse");
        }
        else if (left) {
            r.open("POST", "/api/control/" + target + "/left");
        }
        else if (right) {
            r.open("POST", "/api/control/" + target + "/right");
        }
        else {
            r.open("POST", "/api/control/" + target + "/stop");
        }
        r.send();
    }
};

var control_forward = function() {
    var target = get_target();
    if (target == "") return;
    var r = new XMLHttpRequest();
    r.open("POST", "/api/control/" + target + "/forward");
    r.send();
    reset_color();
    document.getElementById("forward-button").style.backgroundColor = "rgba(234, 250, 241, .75)";
    forward = true;
};

var control_left = function() {
    var target = get_target();
    if (target == "") return;
    var r = new XMLHttpRequest();
    r.open("POST", "/api/control/" + target + "/left");
    r.send();
    reset_color();
    document.getElementById("left-button").style.backgroundColor = "rgba(234, 250, 241, .75)";
    left = true;
};

var control_right = function() {
    var target = get_target();
    if (target == "") return;
    var r = new XMLHttpRequest();
    r.open("POST", "/api/control/" + target + "/right");
    r.send();
    reset_color();
    document.getElementById("right-button").style.backgroundColor = "rgba(234, 250, 241, 1)";
    right = true;
};

var control_reverse = function() {
    var target = get_target();
    if (target == "") return;
    var r = new XMLHttpRequest();
    r.open("POST", "/api/control/" + target + "/reverse");
    r.send();
    reset_color();
    document.getElementById("reverse-button").style.backgroundColor = "rgba(234, 250, 241, 1)";
    reverse = true;
};

var control_stop = function() {
    var target = get_target();
    if (target == "") return;
    var r = new XMLHttpRequest();
    r.open("POST", "/api/control/" + target + "/stop");
    r.send();
    reset_color();
    document.getElementById("stop-button").style.backgroundColor = "rgba(254, 249, 231, 1)";
    forward = false;
    left = false;
    right = false;
    reverse = false;
};

var reset_color = function() {
    document.getElementById("forward-button").style.backgroundColor = "white";
    document.getElementById("left-button").style.backgroundColor = "white";
    document.getElementById("right-button").style.backgroundColor = "white";
    document.getElementById("reverse-button").style.backgroundColor = "white";
    document.getElementById("stop-button").style.backgroundColor = "white";
};

var forward = false;
var left = false;
var right = false;
var reverse = false;
var party = false;

document.getElementById("forward-button").onmousedown = function() {
    if (!forward) {
        control_forward();
    }
};

document.getElementById("left-button").onmousedown = function() {
    if (!left) {
        control_left();
    }
};

document.getElementById("right-button").onmousedown = function() {
    if (!right) {
        control_right();
    }
};

document.getElementById("reverse-button").onmousedown = function() {
    if (!reverse) {
        control_reverse();
    }
};

document.onmouseup = function() {
    control_stop();
};

document.getElementById("forward-button").ontouchstart = function() {
    if (!forward) {
        control_forward();
    }
};

document.getElementById("left-button").ontouchstart = function() {
    if (!left) {
        control_left();
    }
};

document.getElementById("right-button").ontouchstart = function() {
    if (!right) {
        control_right();
    }
};

document.getElementById("reverse-button").ontouchstart = function() {
    if (!reverse) {
        control_reverse();
    }
};

document.ontouchend = function() {
    control_stop();
};

document.onkeydown = function(e) {
    if (e.keyCode == "37") {
        // left arrow
        if (!left) {
            control_left();
        }
    }
    else if (e.keyCode == "38") {
        // up arrow
        if (!forward) {
            control_forward();
        }
    }
    else if (e.keyCode == "39") {
        // right arrow
        if (!right) {
            control_right();
        }
    }
    else if (e.keyCode == "40") {
        // back arrow
        if (!reverse) {
            control_reverse();
        }
    }
    else if (e.keyCode == "80") {
        // p key
        if (party) {
            disable_party_mode();
            party = false;
        }
        else {
            enable_party_mode();
            party = true;
        }
    }
};

document.onkeyup = function(e) {
    if (e.keyCode == "37") {
        // left arrow
        left = false;
        if (forward) {
            control_forward();
        }
        else if (reverse) {
            control_reverse();
        }
    }
    else if (e.keyCode == "38") {
        // up arrow
        forward = false;
    }
    else if (e.keyCode == "39") {
        // right arrow
        right = false;
        if (forward) {
            control_forward();
        }
        else if (reverse) {
            control_reverse();
        }
    }
    else if (e.keyCode == "40") {
        // back arrow
        reverse = false;
    }
    if (!left && !forward && !right && !reverse) {
        control_stop();
    }
};

window.setInterval(check_direction, 250);