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
  }, 
  function(err) {
  	console.error("Error getting JSON", err);
  });
});

console.log("Service workers!");