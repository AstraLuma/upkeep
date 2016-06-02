A basic [web push](https://www.w3.org/TR/push-api/) ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)) handler. It manages associations of subscriptions with Django users. (Anonymous users don't get pushes.)

Give the client-side the named URLs `push:register` and `push:unregister`. Both of these take POSTed JSON containing a single field: URL. (The user must be currently signed in.) If successful (the URL is now registered), a 202 Accepted with an empty JSON object is returned.

Email is also supported in the form of `mailto:` addresses.

The application can use `piston.notify(user, text)` to pass a notification to all subscriptions. The text is only used with email, not WebPush because encryption is hard.

If you wish to enumerate registrations (eg, for management), call `get_registrations(user)`. It'll produce an iterable of `(url, type)` where `type` is one of `"web"` or `"email"`. (More types may be added in the future.)