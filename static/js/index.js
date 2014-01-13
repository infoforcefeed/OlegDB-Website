slogans = [
    "when mission critical just doesn't make any sense.",
    "when you just don't really need master-master replication.",
    "when those other databases are just too relational.",
    "when determinism really isn't your thing.",
    "when JSON is holding you back.",
    "when you want to take a chance.",
    "when concurrency has too much overhead."
];
function fade_change(element, text) {
    var op = 1;
    var timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            element.innerHTML = text;
            element.style.opacity = 0;
            fade_in(element);
        }
        element.style.opacity = op;
        op -= op * 0.1;
    }, 50);
}
function fade_in(element) {
    var op = 0;
    var timer = setInterval(function () {
        if (op >= 1.0){
            clearInterval(timer);
            element.style.opacity = 1.0;
        }
        element.style.opacity = op;
        op += 0.05;
    }, 50);
}
function change_text() {
    var rand = Math.floor(Math.random() * slogans.length);
    change_me = document.getElementById("changing_text");
    fade_change(change_me, slogans[rand]);
    setTimeout(change_text, 4000);
}
window.onload = function() {
    var rand = Math.floor(Math.random() * slogans.length);
    change_me = document.getElementById("changing_text");
    change_me.innerHTML = slogans[rand];
    setTimeout(change_text, 4000);
};
