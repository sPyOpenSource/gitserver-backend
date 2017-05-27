Element.prototype.hasClassName = function(e) {
    return new RegExp("(?:^|\\s+)" + e + "(?:\\s+|$)").test(this.className)
}, Element.prototype.addClassName = function(e) {
    this.hasClassName(e) || (this.className = [this.className, e].join(" "))
}, Element.prototype.removeClassName = function(e) {
    if (this.hasClassName(e)) {
        var t = this.className;
        this.className = t.replace(new RegExp("(?:^|\\s+)" + e + "(?:\\s+|$)", "g"), " ")
    }
}, Element.prototype.toggleClassName = function(e) {
    this[this.hasClassName(e) ? "removeClassName" : "addClassName"](e)
}, document.documentElement.removeClassName("no-js"), document.documentElement.addClassName("js");
var init = function() {
    document.getElementById("more-1").addEventListener("click", function() {
        document.getElementById("list-more-1").toggleClassName("click")
    }, !1), document.getElementById("more-2").addEventListener("click", function() {
        document.getElementById("list-more-2").toggleClassName("click")
    }, !1)
};
if (window.addEventListener("DOMContentLoaded", init, !1)) {

}
