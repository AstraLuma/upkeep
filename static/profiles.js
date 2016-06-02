"use strict";

$$.id('addemailbtn').addEventListener("click", function(event) {
	$$.id('addemailbtn').disabled = true;
    $$.json.post("/!push/register", {
    	url: "mailto:" + $$.id('email').value
    }).then(function() {
	    document.location.reload();
    });
});

$$.q('[data-action=delete-email]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        if (window.confirm("Are you sure you want to stop receiving reminders at "+ele.dataset.label+"?")) {
            console.log("Delete registration", ele.dataset.url);
            $$.json.post("/!push/unregister", {'url': ele.dataset.url})
            .then(function() {
                // TODO: Fade out nicely
                var parent = ele.parentElement;
                parent.parentElement.removeChild(parent);
            });
        }
    });
});
