const { contextBridge, ipcRenderer } = require('electron');

let uuid_reported = "";
ipcRenderer.on('view-conversation-reported', (_, data) => {
    uuid_reported = data;
});

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