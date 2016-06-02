"use strict";

$$.q('[data-action=show-dialog]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        $$.id(ele.dataset.dialog).showModal();
    });
});

$$.q('[data-action=close]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        ele.parentNode.close();
    });
});

