"use strict";
/* Page-side of serviceworkers */

(function() {
  if (navigator.serviceWorker) {
    var serviceWorkerRegistration;
    navigator.serviceWorker.register('/static/service.js' /* need django static */)
    .then(function(swr) { 
      serviceWorkerRegistration = swr; 
      return swr.pushManager.getSubscription(); 
    })
    .then(function(ps) {
      if (ps) return;
      return serviceWorkerRegistration.pushManager.subscribe({userVisibleOnly: true});
    })
    .then(
      function(pushsub) {
        if (!pushsub) return;
        console.log(pushsub.endpoint);
        return $$.json.post("/!push/register", {url: pushsub.endpoint});
      }, function(err) {
        console.error("Can't subscribe!", err); 
        throw err;
    })
    .then(function(resp) {
      console.info("Registered!", resp);
    }, function(err) {console.error("Can't register subscription!", err);});
  }
})();