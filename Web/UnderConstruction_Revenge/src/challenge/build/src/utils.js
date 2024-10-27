const params = new URLSearchParams(location.search);
const debugLevels = { 0:"DEBUG", 1:"INFO", 2:"NOTICE", 3:"WARNING", 4:"ERROR", 5:"CRITICAL", 6:"ALERT", 7:"EMERGENCY" };

function initDefaultData() {
    var defaultData = Object.create(null);
    defaultData.debugLevel = debugLevels[params.get("debugLevel") || 0];
    return defaultData;
}

function deepMerge(target, source) {
    for (const key of Object.keys(source)) {
        if (key === "__proto__" || key === "constructor") {
            continue;
        }
  
        if (source[key] && typeof source[key] === "object" && !Array.isArray(source[key])) {
            if (!target[key] || typeof target[key] !== "object") {
                target[key] = {};
            }
            deepMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

export {
    deepMerge,
    initDefaultData
}