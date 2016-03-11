A basic [web push](https://www.w3.org/TR/push-api/) ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)) handler. It manages associations of subscriptions with Django users. (Anonymous users don't get pushes.)

Give the client-side the named URLs `push:register` and `push:unregister`. TODO: Format

The application can use `piston.notify(user)` to pass a notification to all subscriptions. There is not data associated with it at this time because Chrome/GCM don't support `PushEvent.data` and I don't feel like writing a polyfill.