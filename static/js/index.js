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
    "when you need to dog-food the kool-aid.",
    "when persistence means turning fsync on."
];
function fade_change(element, text) {
    var op = 1;
    var timer = setInterval(function () {
        if (op <= 0.05){
            clearInterval(timer);
            element.innerHTML = "";
            element.style.opacity = 0;
            fade_in(element, text);
        }
        element.style.opacity = op;
        op -= op * 0.2;
    }, 50);
}
function fade_in(element, text) {
    var op = 0;
    var timer = setInterval(function () {
        if (op >= 1.0){
            clearInterval(timer);
            element.style.opacity = 1.0;
            window.setTimeout(change_text, delay);
        }
        if (op == 0) {
            element.innerHTML = text;
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
