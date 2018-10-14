var log = function(s) {
    console.log(s);
    create_log_line(s);
};

var log_date = function(d, s) {
    log("[" + d.toISOString() + "] " + s);
};

var create_log_line = function(s) {
    var e = document.createElement("div");
    e.className = "log-line";
    e.innerHTML = s;
    var area = document.getElementById("logs-area");
    area.appendChild(e);
    area.scrollTop = area.scrollHeight;
};
