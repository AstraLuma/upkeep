A basic [web push](https://www.w3.org/TR/push-api/) ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)) handler. It manages associations of subscriptions with Django users. (Anonymous users don't get pushes.)

Give the client-side the named URLs `push:register` and `push:unregister`. TODO: Format

Email is also supported in the form of `mailto:` addresses.

The application can use `piston.notify(user, text)` to pass a notification to all subscriptions. The text is only used with email, not WebPush because encryption is hard.

