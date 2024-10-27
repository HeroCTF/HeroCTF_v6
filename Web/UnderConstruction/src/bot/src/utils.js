// Colors
const bold      = (str) => `\x1b[1m${str}\x1b[0m`;
const underline = (str) => `\x1b[4m${str}\x1b[0m`;
const red       = (str) => `\x1b[31m${str}\x1b[0m`;
const green     = (str) => `\x1b[32m${str}\x1b[0m`;
const yellow    = (str) => `\x1b[33m${str}\x1b[0m`;
const blue      = (str) => `\x1b[34m${str}\x1b[0m`;
const gray      = (str) => `\x1b[2m${str}\x1b[0m`;
const nothing   = (str) => str;
const getConsoleColor = { "log": green, "warn": yellow, "error": red }

const logMainInfo = (str) => {
    console.log("\n" + underline(str));
}

const delay = (time) => {
    return new Promise(resolve => setTimeout(resolve, time));
}

const hookPageEvents = async (page, id) => {
    page.on("console", (msg) => {
        var msgType = msg.type();
        var color   = getConsoleColor[msgType] || nothing;
        console.log(`${bold(`[T${id}]>`)} ${color(`console.${msgType}`.padEnd(17))} ${bold("|")} ${msg.text()}`);
    });

    page.on("framenavigated", (frame) => {
        if (frame === page.mainFrame()) {
            console.log(`${bold(`[T${id}]>`)} ${blue("navigating".padEnd(17))} ${bold("|")} ${frame.url()}`);
        }
    });
}

// Workaround of https://github.com/puppeteer/puppeteer/blob/237cb42b34fca582a69386a610e185159564a43f/packages/puppeteer-core/src/cdp/Target.ts#L299
// Thanks @Drarig29: https://stackoverflow.com/questions/73407885/how-can-i-forward-service-worker-console-logs-to-stdout-in-the-terminal
const hookWorkerEvents = async (worker, id) => {
    worker.client.on("Runtime.consoleAPICalled", (args) => {
        var msgType = args.type;
        var color   = getConsoleColor[msgType] || nothing;
        console.log(`${bold(`[S${id}]>`)} ${color(`console.${msgType}`.padEnd(17))} ${bold("|")} ${args.args[0].value}`);
    });
}

let nbTab = 0;
let nbSW  = 0;
const handleTargetCreated = async (target) => {
    if (target.type() === "page") {
        nbTab++;
        console.log(`${bold(`[T${nbTab}]>`)} ${gray("New tab created!")}`);
        const page = await target.page();
        console.log(`${bold(`[T${nbTab}]>`)} ${blue("navigating".padEnd(17))} ${bold("|")} ${page.url()}`);
        await hookPageEvents(page, nbTab);
    } else if (target.type() === "service_worker") {
        nbSW++
        console.log(`${bold(`[S${nbSW}]>`)} ${gray("New Service Worker created!")}`);
        const worker = await target.worker();
        await hookWorkerEvents(worker, nbSW);
    }
}

module.exports = {
    delay,
    handleTargetCreated,
    logMainInfo
}