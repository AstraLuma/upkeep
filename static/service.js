/* Service Worker */
"use strict";

self.addEventListener('push', function(event) {
  console.info("Pushed!");
  // Safely reentrant; don't use waituntil()
  fetch("/undones.json", {credentials: 'same-origin'})
  .then(function(resp) {
    console.info("Got response", resp);
    return resp.json()
  })
  .then(function(obj) {
    console.info("Undones", obj);

    // Have to pull out the latest, notify on that

    var title = 'New Job';  
    var body = 'You have '+obj.jobs.length+' jobs';
    var icon = 'push-icon.png';  
    var tag = 'new-job';
   
    return self.registration.showNotification(title, {
      body: body,  
      icon: icon,  
      tag: tag  
    });
  })
  .then(function(event) {
    console.info("Notification", event);
  });
});

console.log("Service workers!");