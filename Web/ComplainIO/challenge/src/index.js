const express = require('express');
const fileUpload = require('express-fileupload');
const app = express();
const path = require("path");
const bodyParser = require("body-parser");
app.use(express.json());
app.use(fileUpload());
app.use(express.static(path.join(__dirname,'public')));
app.disable('x-powered-by');
require("./routes/complain.routes")(app);

const PORT = 3000;

app.get('/', (_, res) => {
  res.sendFile(path.join(__dirname,'/views/index.html'));
});

app.get('/profile', (_, res) => {
  res.sendFile(path.join(__dirname,'/views/profile.html'));
})

app.get('/complain', (_, res) => {
  res.sendFile(path.join(__dirname,'/views/complain.html'));
})

app.listen(PORT, () => {
    console.log(`Sales management application is running on port ${PORT}.`);
});