/* Service Worker */
"use strict";

self.addEventListener('push', function(event) {
  console.info("Pushed!");
  // This is safely reentrant; waitUntil is not necessary
  fetch("/undones.json", {credentials: 'same-origin'})
  .then(function(resp) {
    console.info("Got response", resp);
    return resp.json()
  })
  .then(function(obj) {
    console.info("Undones", obj);

    var jobs = obj.jobs;
    console.info("Jobs", jobs);

    if (jobs.length < 1) {
      console.info("Ok, we lied. We're not going to show a notification");
      return;
    }

    var curjob = jobs[0];
    jobs.forEach(function(job) {
      console.info("Job", job);
      if (curjob.when < job.when)
        curjob = job;
    });

    console.info("curjob", curjob);

    var title = 'New Job: '+curjob.schedule.name;
    var ops = {
      'body':  'Plus '+(obj.jobs.length - 1)+' other jobs',
      'icon': 'push-icon.png',
      'tag': 'new-job'
    };
    
    console.info("ops", ops);

    return self.registration.showNotification(title, ops)
    .then(function(event) {
      console.info("Notification", event);
      // This is failing. Not sure why.
      return clients.openWindow(curjob.schedule.url);
    }, function(err) {console.error("Notification problems", err); throw err;});
  }).then(
  function(obj) {console.log("Resolve", obj);},
  function(obj) {console.error("Reject", obj);}
  );
});

console.log("Service workers!");