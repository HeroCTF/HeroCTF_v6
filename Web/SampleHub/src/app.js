const express = require("express");
const path    = require("path");

const app  = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, "public")));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.get("/", (req, res) => {
    res.render("index");
});

process.chdir(path.join(__dirname, "samples"));
app.get("/download/:file", (req, res) => {
    const file = path.basename(req.params.file);
    res.download(file, req.query.filename || "sample.png", (err) => {
        if (err) {
            res.status(404).send(`File "${file}" not found`);
        }
    });
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
