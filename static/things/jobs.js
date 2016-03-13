$$.q('[data-action=finish-job]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        var jobid = event.target.dataset.jobid;
        $$.json.post("/finish.json", {'job': jobid})
        .then(function() {
            event.target.innerText = "Ok!";
            event.target.disabled = true;
        });
    });
});

$$.q('[data-action=show-dialog]').forEach(function(ele) {
    ele.addEventListener("click", function(event) {
        $$.id(event.target.dataset.dialog).showModal();
    });
});
