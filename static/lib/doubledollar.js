/*
                                      `\\  \\     !||
                                    \  \\\\\\\\,  !||
                                 \,,.\\\,\ ,\ |\\/!||
                                 \\V\ ,\ V \\| |//!||    
                                 \\VVVV\\\V/ |/  //||     
                                    VVVV\\((-\\./ /||     
                                    \VVV_\\==- ''/|FF|    
                                     \V( \   .,  ,|JL|    
                                      \_\|     (( \||/
                                      .  |      / ,|| \
                                   __;__ `. `--' ( LJ )\
                                  [""""""""`._/  |)  /".)
                                  )``    """'-"")(   "./
                            _,-,-"'-.__  __,--;""-,-,_ (
                       _.-"( (         ""       / (  "._  
                      / |  |o(                 /o/    ,"" 
                     (  |  '-"                 \/  /(   )
                     |\ :                         /    (
                    ["  \                        ".   _ |
                     `--.\                         "." ""
                     /_  :                         \   //.
                    [==--,\   ,-.           ,-.    )    ;   
                    /  ``/`\  \O \   ,-.   / O/   /     ;
                    :   |  :   \  \." | ",/  /   ;     ;
                   [====]   \  ,\  \  |("`_,/.  /.     ;
                   }   "/    \/  ) (__{/  \____\/ \    ;
                   "__ |         \_,_ / O/      "-.\__/   
                  ,'  `.        __|  /" !,\______,'_ 
                  :    ;]      (  ,--' _"  `.    "_,".
                   ;--'(       / /  _,'  ;   `.    / (
                   [===]'    _;-' ,'  |   `.   \   (  |.
                   '    ;  .' o_,'    |     \ o `.__|_.';
                    :   ;  \o,'       |      `._  o  o /
                    [ctr]   \(        |         `-----/
                     [===]   ;        \             | |
                     ;   \   |         \            | |
                     )   ,\  ;         |            | :
                     |  /((  |         |            : |
                     \\ ;_,  |         |            | |
                     ``---`  ;         |            | :
                            ;'         |            : `:
                            |          ;            `: |
                            |       :  ;           __|_|
                            ;        :;'          [o_|o/
                           ;' :      ::            ` :``:
                           |  :       :              :  |
                          ;  .:       \         :    `: |
                          | .:   ;    `;.       :     : |
                          | :    ;      :       :     : |
                          | :    ;      |       |     : '.
                          ; :   ,;      |       :.    :  :
                         ;' :   ;       :        :    '. '.
                         |      |       \        :     \  :
                        /|      ;       `\       |     || |
                       ; |      |        `|      :.    || |
                       | :      |         |       |    || |
                       | |      |         |       :    ||.'.
                       ; ;      ;         ;       :    ':| |
                      /  /      |   ___   |       :     || :
                      ;' |      ;"-"!!8"",;       :     || |
                      | /|      \ !,##/!8!/,      |     || |
                      |/#'._     )!#[]#!88\|      :     ||  \
                      \|    `-,-' !#==#!88|`      :,-.__||,-'
                       `          ,####.""""7"",---'
                                  #====#   ;___ (,_._
                                  ######   [_____/o/==._
                                  `#==#'   \     ""__ __)
                                   `##'    |####|-######

           doubledollar.js - The sixty billion double-dollar JavaScript library.

I think of this as jQuery lite. It helps with some really common stuff but 
largely just supplements vanilla DOM. Uses promises extensively.
*/
"use strict";

var $$ = {};

// Create a namespace for global constants
(function($$) {

/** {{{ DOM wrappers **/

/**
 * Create an element, returning it.
 */
$$.createElement = function(tag, attrs, children) {
    var ele = document.createElement(tag);

    if (attrs) {
        for(a in attrs) {
            ele.setAttribute(a, attrs[a]);
        }
    }

    if (children) {
        children.forEach(function(kid) {
            ele.appendChild(kid);
        });
    }

    return ele;
};

/// Shortcut for $$.createElement().
$$.e = $$.createElement;

/**
 * Creates a text node, returning it.
 */
$$.createText = function(txt) {
    return document.createTextNode(txt);
};

/// Shortcut for $$.createText().
$$.t = $$.createText;

/**
 * Performs a CSS query, returning an Array (not NodeList) of selected elements.
 * 
 * Comes in two forms:
 *  - $$.query(element, expr) to search under an element (also works with 
 *    DocumentFragments, Shadow Roots, non-default Documents, etc)
 *  - $$.query(expr) to search the main Document
 */
$$.query = function(ele, expr) {
    var nl;
    if (!expr) {
        // ele is actually the expression
        expr = ele;
        ele = document;
    }
    nl = ele.querySelectorAll(expr);


    // NodeLists are super lame to work with. Hopefully, this copy isn't too bad.
    var rv = new Array(nl.length);
    for (var i = 0; i < nl.length; i++) {
        rv[i] = nl.item(i);
    }

    return rv;
};

/// Shortcut for $$.query
$$.q = $$.query;

/**
 * Empties an element, moving all of its children to a document fragment.
 *
 * This is useful for rebuilding the contents of a custom tag. You can get 
 * the children out of the way and then select on them.
 *
 * Note: This uses the document of the original element.
 */
$$.empty2fragment = function(ele) {
    var df = ele.ownerDocument.createDocumentFragment();
    // Waaaay too side-effect heavy for my taste, but compact and hopefully efficient.
    while(ele.firstChild) {
        df.appendChild(ele.firstChild);
    }
    return df;
};

/** }}} **/

/** {{{ AJAX **/

/**
 * Basic AJAX wrapper method.
 *
 * - method: GET, POST, PUT, ...
 * - url: URL to send the request to
 * - options.params: Object of parameters to add to the URL
 * - options.body: Content to send to request
 * - options.headers: Object of headers to add to the request
 * - options.responseType: Passed directly to XHR
 * - options.withCredentials: "Indicates whether or not cross-site 
 *   Access-Control requests should be made using credentials such as cookies or
 *   authorization headers. The default is false." (MDN)
 * - options.timeout: How long to wait (in milliseconds) before failing the request
 * - options.progress: Function to call with progress events
 *
 * The returned promise is resolved if the HTTP request completes, regardless of
 * the status code. It is rejected if the request fails.
 */
$$.ajax = function(method, url, options) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        method = method.toUpperCase();

        if (options.params) {
            url += (url.indexOf('?') > 0 ? '&' : '?') + options.params;
        }

        xhr.open(method, url, true);

        if (options.responseType) {
            xhr.responseType = options.responseType;
        }
        if (options.withCredentials) {
            xhr.withCredentials = true;
        }

        if (options.headers) {
            for (var h in options.headers) {
                xhr.setRequestHeader(h, options.headers[h]);
            }
        }
        // This bit is Django-specific. If you copy this library, you'll probably want to remove it
        xhr.setRequestHeader('X-CSRFToken', $$.getCookies().csrftoken);

        if (options.progress) {
            xhr.addEventListener("progress", options.progress, false);
        }

        xhr.addEventListener("load", function() {
            if (200 <= xhr.status && xhr.status < 400) {
                resolve(xhr);
            } else {
                reject(xhr);
            }
        }, false);
        
        xhr.addEventListener("error", function() {
            reject(xhr);
        }, false);
        
        xhr.addEventListener("abort", function() {
            reject(xhr);
        }, false);

        xhr.addEventListener("timeout", function() {
            reject(xhr);
        }, false);

        var body = options.body;
        if ($$.isPlainObject(options.body)) {
            body = new FormData();
            for (f in object.body) {
                body.append(f, object.body[f]);
            }
        }

        xhr.send(body);
    });
};

/**
 * Shortcut to execute a GET.
 */
$$.get = function(url, params, options) {
    if (!options) {
        options = {};
    }
    options.params = params;
    return $$.ajax('GET', url, options);
};

/**
 * Shortcut to execute a POST
 */
$$.post = function(url, body, options) {
    if (!options) {
        options = {};
    }
    options.body = body;
    return $$.ajax('POST', url, options);
};

// Not including PUT, DELETE, or others because the precise requests are heavily customized

/** {{{ JSON Requests **/

$$.json = {
    get: function(url, params, options) {
        if (!options) {
            options = {};
        }
        options.params = params;
        options.responseType = "json";
        return $$.ajax('GET', url, options);
    },
    post: function(url, body, options) {
        if (!options) {
            options = {};
        }
        if (!options.headers) {
            options.headers = {};
        }
        options.body = JSON.stringify(body);
        options.headers['Content-Type'] = 'application/json';
        options.responseType = "json";
        return $$.ajax('POST', url, options);
    },
    put: function(url, body, options) {
        if (!options) {
            options = {};
        }
        if (!options.headers) {
            options.headers = {};
        }
        options.body = JSON.stringify(body);
        options.headers['Content-Type'] = 'application/json';
        options.responseType = "json";
        return $$.ajax('PUT', url, options);
    },
    delete: function(url, options) {
        if (!options) {
            options = {};
        }
        options.responseType = "json";
        return $$.ajax('DELETE', url, options);
    }
};

/** }}} **/

/** }}} **/

/** {{{ Promise Utilities **/

/**
 * Reject a promise after a delay (in milliseconds).
 *
 * Use cases include implementing timeouts with Promise.race().
 */
$$.timeout = function(ms, reason) {
    return new Promise(function(resolve, reject) {
        window.setTimeout(reject, ms, reason);
    });
};

/**
 * Resolve a promise after a delay (in milliseconds).
 */
$$.delay = function(ms, result) {
    return new Promise(function(resolve, reject) {
        window.setTimeout(resolve, ms, result);
    });
};

/**
 * Get a resolved promise.
 *
 * Useful for calling a function outside the current event (ie, asyncronous tasks)
 * instead of using window.setTimeout(0, ...).
 */
$$.immediate = function() {
    return Promise.resolve();
};

/** }}} */

/** {{{ Promise-based Web API wrappers */

/** 
 * Returns a promise that resolves with the system-scheduled frame. Resolves 
 * with the time as the result.
 *
 *(Promise-based wrapper around window.requestAnimationFrame.)
 */
$$.frame = function() {
    return new Promise(function(resolve, reject) {
        window.requestAnimationFrame(resolve);
    });
}

/**
 * Promises the user's location.
 *
 * Resolves with a Position object.
 * Rejects with a PositionError object.
 *
 * - options: A PositionOptions object.
 */
$$.location = function(options) {
    return new Promise(function(resolve, reject) {
        navigator.geolocation.getCurrentPosition(resolve, reject, options);
    });
}

/** }}} **/

/** {{{ Utilities **/
$$.isPlainObject = function (o) {
    // From https://stackoverflow.com/questions/5876332/how-can-i-differentiate-between-an-object-literal-other-javascript-objects
    return typeof o == 'object' && o.constructor == Object;
};

var rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;
$$.trim = function( text ) {
    return text == null ?
        "" :
        ( text + "" ).replace( rtrim, "" );
};

$$.getCookies = function () {
    var cookiejar = {};
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $$.trim(cookies[i]);
            cookie = cookie.split('=', 2);
            cookiejar[cookie[0]] = decodeURIComponent(cookie[1]);
        }
    }
    return cookiejar;
}

/** }}} **/

})($$);