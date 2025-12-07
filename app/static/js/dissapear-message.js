// suppose the `id` attribute of element is `message-div`.
var message_ele = document.getElementById("message-div");

setTimeout(function () {
    message_ele.style.display = "none";
}, 3000);
// Timeout is 3 sec, you can change it