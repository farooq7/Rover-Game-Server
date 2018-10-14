var continue_display = false;
var x_min = 101, x_max = 529, y_min = 0, y_max = 389;

var enable_display = function() {
    continue_display = true;
};

var disable_display = function() {
    continue_display = false;
};

var update_display = function() {
    if (!continue_display) {
        return;
    }
    draw_tokens();
    if (window.localStorage.getItem("blue_ip") != "") {
        draw_location(window.localStorage.getItem("blue_ip"), document.getElementById("blue-img"));
    }
    if (window.localStorage.getItem("red_ip") != "") {
        draw_location(window.localStorage.getItem("red_ip"), document.getElementById("red-img"));
    }
};

var draw_location = function(target, img) {
    if (img == null) {
        return;
    }
    if (target == null) {
        img.style.display = "none";
        return;
    }
    var r = new XMLHttpRequest();
    r.open("POST", "/api/last_location/" + target);
    r.send();
    r.onload = function() {
        if (r.status != 200) {
            console.log("Unable to get location.");
            return;
        }
        o = JSON.parse(r.responseText);
        if (o == null) {
            img.style.display = "none";
            return;
        }
        var x = o["x"];
        var y = o["y"];
        var degrees = o["rotation"];
        console.log(target + " found at (" + x + ", " + y + ").");
        var tx = tmap(x, 0, 200, x_min, x_max);
        var ty = tmap(y, 0, 200, y_min, y_max);
        if (tx < x_min + img.width / 2) {
            tx = x_min + img.width / 2;
        }
        if (tx > x_max - img.width / 2) {
            tx = x_max - img.width / 2;
        }
        if (ty < y_min + img.height / 2) {
            ty = y_min + img.height / 2;
        }
        if (ty > y_max - img.height / 2) {
            ty = y_max - img.height / 2;
        }
        img.style.left = tx + "px";
        img.style.top = ty + "px";
        img.style.transform = "translate(-50%, -50%) rotate(" + degrees + "deg)";
        img.style.display = "inline";
    }
};

var draw_tokens = function() {
    var r = new XMLHttpRequest();
    r.open("POST", "/api/get_tokens");
    r.send();
    r.onload = function() {
        if (r.status != 200) {
            console.log("Unable to get tokens.");
            return;
        }
        var tokens = JSON.parse(r.responseText);
        for (var i = 0; i < tokens.length; i++) {
            var token = tokens[i];
            if (token["color"] == "black") {
                continue;
            }
            var id = translate_id(token['name']);
            var img = document.getElementById(id);
            if (token["collected"])
            {
                if (img != null) {
                    img.style.display = "none";
                }
            }
            else
            {
                var x = token["x"];
                var y = token["y"];
                var tx = tmap(x, 0, 200, x_min, x_max);
                var ty = tmap(y, 0, 200, y_min, y_max);
                var img = document.getElementById(id);
                if (img == null) {
                    img = document.createElement("img");
                    img.id = id;
                    img.src = "/static/img/" + token["color"] + ".png";
                    img.style.position = "absolute";
                    img.style.width = "16px";
                    img.style.height = "16px";
                    img.style.left = tx + "px";
                    img.style.top = ty + "px";
                    document.getElementById("display-canvas").appendChild(img);
                }
                else {
                    img.style.left = tx + "px";
                    img.style.top = ty + "px";
                }
                img.style.display = "inline";
            }
        }
    };
};

var translate_id = function(id) {
    return id.replace(" ", "_").toLowerCase();
};

var tmap = function(x, in_min, in_max, out_min, out_max) {
    return (((x - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min);
};

window.setInterval(update_display, 500);