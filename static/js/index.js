index = 0;
delay = 4000;
slogans = [
    "when mission critical just doesn't make any sense.",
    "when you just don't need multi-master replication.",
    "when those other databases are just too relational.",
    "when you're not quite sure what web scale means.",
    "when determinism really isn't your thing.",
    "when JSON is holding you back.",
    "when you want to take a chance.",
    "when persistence means turning fsync on."
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
            window.setTimeout(change_text, delay);
        }
        element.style.opacity = op;
        op += 0.05;
    }, 50);
}
function change_text() {
    index++;
    change_me = document.getElementById("changing_text");
    fade_change(change_me, slogans[index % slogans.length]);
}
window.onload = function() {
    change_me = document.getElementById("changing_text");
    rand_int = Math.floor(Math.random()*slogans.length);
    change_me.innerHTML = slogans[rand_int];
    window.setTimeout(change_text, delay);
};
