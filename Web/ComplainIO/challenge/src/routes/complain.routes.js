module.exports = app => {
    const usersController = require("../controllers/users.controller.js");
    const filesController = require("../controllers/files.controller.js");
    const complainsController = require("../controllers/complains.controller.js")
  
    var router = require("express").Router();

    router.post("/login", usersController.login);
    router.post("/register", usersController.register);
    router.patch("/profile", usersController.profile);
    router.post("/upload", usersController.upload);
    router.get("/me", usersController.me);

    router.post("/create_template", filesController.createTemplate);
    router.get("/picture/:uuid", filesController.getProfilePicture);

    router.get('/complains', complainsController.getAll);

    app.use("/api", router);
};