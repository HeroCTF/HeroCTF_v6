const { app, BrowserWindow, session } = require('electron');
const path = require('path');

let mainwin;
let deeplinkUrl;

const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
    app.quit();
} else {
    app.on('second-instance', (event, commandLine) => {
        deeplinkUrl = commandLine.find((arg) => arg.startsWith('telechat://'));
        if (mainwin) {
            if (mainwin.isMinimized()) mainwin.restore();
            mainwin.focus();
            if (deeplinkUrl) {
                mainwin.webContents.send('deeplink', deeplinkUrl);
            }
        }
    });

    function createWindow() {
        mainwin = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                preload: path.resolve(__dirname, 'preload.js'),
                contextIsolation: true,
                nodeIntegration: false,
                sandbox: true
            }
        });

        mainwin.loadFile('index.html');

        if (deeplinkUrl) {
            mainwin.webContents.send('deeplink', deeplinkUrl);
        }
    }

    app.whenReady().then(() => {
        createWindow();

        const args = process.argv.slice(1);
        deeplinkUrl = args.find((arg) => arg.startsWith('telechat://'));
        if (deeplinkUrl) {
            mainwin.webContents.send('deeplink', deeplinkUrl);
        }

        const ses = session.defaultSession;

        ses.on('will-download', (_, item, __) => {
            let filePath = path.join(app.getPath('downloads'), Math.random().toString(36).substring(2, 15), item.getFilename());
            filePath = path.normalize(Buffer.from(filePath, "ascii").toString());
            item.setSavePath(filePath);
           
        });

        app.on('activate', () => {
            if (BrowserWindow.getAllWindows().length === 0) {
                createWindow();
            }
        });
    });

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            app.quit();
        }
    });
}