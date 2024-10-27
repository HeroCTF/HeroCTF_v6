const http = require('http');
const socketIo = require('socket.io');
const sqlite3 = require('sqlite3');
const { open } = require('sqlite');
const url = require('url');
const { spawn } = require('child_process');

function sanitize(str) {
    return str.replace(/[^a-zA-Z0-9]/g, '');
}

async function setupDatabase() {
    const db = await open({
        filename: './db.sqlite',
        driver: sqlite3.Database
    });

    await db.exec(`
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE
        );
    `);

    await db.exec(`
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            conv_id INTEGER,
            FOREIGN KEY (conv_id) REFERENCES conversations (id)
        );
    `);

    return db;
}

const dbPromise = setupDatabase();
const port = process.env.PORT || 3000;
const messages = ["I can't help you with this... Any others questions ?", "This is inappropriate.", "[BIP BOUP] : ERROR"];
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

const io_user = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const io_bot = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    },
    path: "/reviews/"
});

io_user.on('connection', (socket) => {
    socket.on('message', async ({ report, uuid, message }) => {
        if (report == 1) {
            socket.emit('response', 'We are reviewing your report...');
            spawn("xdg-open",[`telechat://review/${message}`]);
            socket.emit('response', 'Our analysis is finished, thank you for reporting.');
        } else {
            const db = await dbPromise;
            await db.run('INSERT OR IGNORE INTO conversations (uuid) VALUES (?)', uuid);
            let result = await db.get("SELECT id FROM conversations WHERE uuid = ?", uuid);
            const conv_id = result.id;
            await db.run('INSERT INTO messages (message, conv_id) VALUES (?, ?)', sanitize(message), conv_id);
            const resp_bot = messages[Math.floor(Math.random() * messages.length)];
            await db.run('INSERT INTO messages (message, conv_id) VALUES (?, ?)', resp_bot, conv_id);
            socket.emit('response', resp_bot);
        }
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});

io_bot.on('connection', async (socket) => {
    const uuid = socket.handshake.url.split('/')[2];
    if (uuid != undefined) {
        const db = await dbPromise;
        let result = await db.get("SELECT id FROM conversations WHERE uuid = ?", uuid);
        if (result) {
            const conv_id = result.id;
            result = await db.all("SELECT message FROM messages WHERE conv_id = ?", conv_id);
            if (result.length > 0) {
                for (var i = 0; i < result.length; i++) {
                    if (result[i] !== undefined) {
                        if (i % 2 == 0) {
                            socket.emit('response', "USER: " + result[i].message);
                        } else {
                            socket.emit('response', "BOT: " + result[i].message);
                        }
                    }
                }
                socket.emit('response','END REVIEW');
            } else {
                socket.emit('response', 'SERVER - [NO DATA]');
            }
        } else {
            socket.emit('response', 'SERVER - [NO DATA]');
        }
    }

    socket.on('disconnect', () => {
        console.log('Review finished')
    });
});

server.listen(port, "0.0.0.0", () => {
    console.log(`Server is running on http://localhost:${port}`);
});
