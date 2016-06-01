"use strict";

$$.q('[data-action=finish-job]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        var jobid = ele.dataset.jobid;
        $$.json.post("/finish.json", {'job': jobid})
        .then(function() {
            ele.innerText = "Ok!";
            ele.disabled = true;
        });
    });
});

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

$$.q('[data-action=delete-schedule]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        if (window.confirm("Are you sure you want to remove your "+ele.dataset.label+"?")) {
            console.log("Delete schedule", ele.dataset.schedule);
            $$.json.post("/delete-schedule.json", {'schedule': ele.dataset.schedule})
            .then(function() {
                // TODO: Fade out nicely
                var parent = ele.parentElement;
                parent.parentElement.removeChild(parent);
            });
        }
    });
});

$$.q('[data-action=delete-thing]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        if (window.confirm("Are you sure you want to remove your "+ele.dataset.label+"?")) {
            console.log("Delete thing", ele.dataset.thing);
            $$.json.post("/delete-thing.json", {'thing': ele.dataset.thing})
            .then(function() {
                // XXX: This is only right if we're deleting the "self" object of the page, rendering the entire page 404
                document.location = "/";
            });
        }
    });
});
