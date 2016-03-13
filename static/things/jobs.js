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
