const path = require("path");

module.exports = {
  entry: "./src/main.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "../apache/static/"),
    publicPath: "auto",
    chunkFilename: "[contenthash].js"
  },
  target: "web",
  mode: "production",
};