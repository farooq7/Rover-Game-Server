
var last_notification_datetime = new Date();
var continue_notifications = false;

var enable_notifications = function() {
    continue_notifications = true;
};

var disable_notifications = function() {
    continue_notifications = false;
};

var update_notifications = function() {
    if (!continue_notifications) {
        return;
    }
    var r = new XMLHttpRequest();
    r.open("POST", "/api/notifications/" + last_notification_datetime.toISOString());
    r.send();
    r.onload = function() {
        if (r.status != 200) {
            console.log("Unable to get notifications.");
            return;
        }
        o = JSON.parse(r.responseText);
        notifications = o["notifications"];
        for (var i = 0; i < notifications.length; i++) {
            last_notification_datetime = new Date(notifications[i]["datetime"]);
            log_date(last_notification_datetime, translate_ip(notifications[i]["text"]));
        }
    }
};

var translate_ip = function(s) {
    if (window.localStorage.getItem("red_ip") != "") {
        s = s.replace(window.localStorage.getItem("red_ip"), "Red");
    }
    if (window.localStorage.getItem("blue_ip") != "") {
        s = s.replace(window.localStorage.getItem("blue_ip"), "Blue");
    }
    return s;
};

window.setInterval(update_notifications, 500);