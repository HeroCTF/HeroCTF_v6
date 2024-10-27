if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/c/sw.js", { scope: "/c/" });
}

import("./utils.js").then((module) => {;
    var defaultData = module.initDefaultData();
    var data = module.deepMerge(defaultData, JSON.parse(document.getElementById("userInfo").innerText));

    module.loggingPath ??= "/c/log.php";
    fetch(`${module.loggingPath}?${JSON.stringify(data)}`, {
        redirect: "manual",
        credentials: "omit",
        cache: "no-cache"
    })
})