const { delay, handleTargetCreated, logMainInfo } = require("./utils");
const puppeteer = require("puppeteer");

// Banner
const tips = ["Every console.log usage on the bot will be sent back to you :)"];
console.log(`==========\nTips: ${tips[Math.floor(Math.random() * tips.length)]}\n==========`);

// Spawn the bot and navigate to the user provided link
async function goto(url) {
    logMainInfo("Starting the browser...");
	const browser = await puppeteer.launch({
		headless: "new",
		ignoreHTTPSErrors: true,
		args: [
			"--no-sandbox",
            "--incognito",
            "--disable-gpu",
            "--disable-jit",
            "--disable-wasm",
            "--disable-dev-shm-usage",
            "--unsafely-treat-insecure-origin-as-secure=http://underconstruction_revenge_web:8000" // serviceWorker.register is only expose on secure contexts. See: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
		],
		executablePath: "/usr/bin/chromium-browser"
	});

    // Hook tabs events
    browser.on("targetcreated", handleTargetCreated);
	const page = await browser.newPage();
	await page.setDefaultNavigationTimeout(5000);

    /* ** CHALLENGE LOGIC ** */
    // Don't lose your time the race should be almost possible to reach (and my risk to impact our infra), and not part of the challenge...
    browser.on("targetcreated", async (target) => {
        const pages = await browser.pages();
        if (pages.length > 3) {
            const newPage = await target.page();
            if (newPage) {
                logMainInfo("New tab limit reach closing it...");
                await newPage.close();
            }
        }
    });

	try {
	    await page.goto(url);
	} catch {}
    await delay(5000);

    logMainInfo("Closing all pages...");
    const pages = await browser.pages();
    for (let p of pages) {
        if (p !== page) {
            await p.close();
        }
    }

    logMainInfo("Going to the /flag page...");
    await page.setCookie({
        name: "FLAG",
        value: process.env.FLAG,
        path: "/",
        httpOnly: true,
        samesite: "Strict",
        domain: "underconstruction_revenge_web"
    });
    await page.goto("http://underconstruction_revenge_web:8000/flag");
    await delay(3000);

    console.log("\nLeaving o/");
    browser.close();
	return;
}

// Handle TCP data
process.stdin.on("data", (data) => {
    const url = data.toString().trim();

    if (!url || !(url.startsWith("http://") || url.startsWith("https://"))) {
        console.log("[ERROR] Invalid URL!");
        process.exit(1);
    }

    goto(url).then(() => process.exit(0));
});
