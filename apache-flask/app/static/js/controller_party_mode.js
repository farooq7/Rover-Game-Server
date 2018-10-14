var winner_audio = new Audio('/static/audio/winner_audio.mp3');

var enable_party_mode = function() {
    document.getElementById("img-cover").style.opacity = 0;
    document.getElementById("party-backdrop").style.opacity = 1;
    document.getElementById("logs-area").style.backgroundColor = "rgba(192, 192, 192, .2)";
    document.getElementById("game-buttons-label").style.color = "white";
    document.getElementById("direction-buttons-label").style.color = "white";
    winner_audio.play();
;}

var disable_party_mode = function() {
    document.getElementById("party-backdrop").style.opacity = 0;
    document.getElementById("img-cover").style.opacity = 0;
    document.getElementById("logs-area").style.backgroundColor = "rgba(250, 250, 250, 1)";
    document.getElementById("game-buttons-label").style.color = "rgb(16, 16, 16)";
    document.getElementById("direction-buttons-label").style.color = "rgb(16, 16, 16)";
    winner_audio.pause();
};