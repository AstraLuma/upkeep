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
        if (window.confirm("Are you sure you want to delete "+ele.dataset.label+"?")) {
            console.log("Delete schedule", ele.dataset.schedule);
        }
    });
});

$$.q('[data-action=delete-thing]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        if (window.confirm("Are you sure you want to delete "+ele.dataset.label+"?")) {
            console.log("Delete thing", ele.dataset.thing);
        }
    });
});
