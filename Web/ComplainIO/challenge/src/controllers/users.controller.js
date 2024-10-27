const db = require("../models");
const { createHash } = require('crypto');
const utils = require("../utils");
const { v4: uuidv4 } = require('uuid');
const Users = db.Users;
const Files = db.Files;
const UPLOADS_DIR = "/tmp/files/"
const fs = require("fs");

exports.login = async (req, res) => {
    if(req.body.username !== undefined && req.body.password !== undefined && 
        typeof(req.body.username) === "string" && typeof(req.body.password) === "string") {
        const user = await Users.findOne({where: {username: req.body.username}});
        if(user === null) {
            res.status(400).send({
                data:
                    "The username or password is incorrect."
            });
        } else {
            if(createHash('sha256').update(req.body.password).digest('hex') === user.password) {
                res.status(200).send({
                    data:
                        "User connected",
                    token:
                        utils.sign_jwt({username: req.body.username})
                })
            } else {
                res.status(400).send({
                    data:
                        "The username or password is incorrect."
                });
            }
        }
    } else {
        res.status(400).send({
            data:
                "Bad request."
        });
    }
}

exports.register = async (req, res) => {
    if(req.body.username !== undefined && req.body.password !== undefined && req.body.firstname !== undefined && req.body.lastname !== undefined &&
        typeof(req.body.username) === "string" && typeof(req.body.password) === "string" && typeof(req.body.firstname) === "string" && typeof(req.body.lastname) === "string") {
            const user = await Users.findOne({where: {username: req.body.username}});
            if(user === null) {
                const created_user = await Users.create({
                    username: req.body.username, 
                    password: createHash('sha256').update(req.body.password).digest('hex'), 
                    firstname: req.body.firstname,
                    lastname: req.body.lastname
                });
                if(created_user.id === null) {
                    res.status(500).send({
                        data:
                            "Internal Server Error."
                    });
                } else {
                    res.status(200).send({
                        data:
                            "User created."
                    });
                }
            } else {
                res.status(400).send({
                    data:
                        "User already exists."
                });
            }
    } else {
        res.status(400).send({
            data:
                "Bad request."
        });
    }
}

exports.me = async (req, res) => {
    let decoded = utils.verify_jwt(req);
    if(decoded.username) {
        const user = await Users.findOne({where: {username: decoded.username}, attributes: ['id', 'username', 'firstname', 'lastname']});
        if(user) {
            let infos = {"id": user.id, "lastname": user.lastname, "firstname": user.firstname, "username": user.username, "pp": null};
            const potential_picture = await Files.findOne({where: {user_id: user.id}, attributes: ['uuid']});
            if(potential_picture) {
                infos["pp"] = potential_picture.uuid;
            }
            res.status(200).send(infos);
        } else {
            res.status(500).send({
                data:
                    "Internal Server Error."
            });
        }
    } else {
        res.status(401).send({
            data:
                "Then token is invalid or was not provided."
        }); 
    }
}

exports.profile = async (req, res) => {
    if(req.body.id !== undefined && req.body.username !== undefined && req.body.firstname !== undefined && req.body.lastname !== undefined &&
       typeof(req.body.id) === "number" && typeof(req.body.username) === "string" && typeof(req.body.firstname) === "string" && typeof(req.body.lastname) === "string") {
        let user_database_content = await Users.findByPk(req.body.id);
        if(user_database_content === null) {
            res.status(404).send({
                data: "User not found."
            });
        } else {
            let decoded = utils.verify_jwt(req);
            if(decoded.username) {
                let current_user = await Users.findOne({where: {username: decoded.username}});
                if(current_user.id != req.body.id) {
                    res.status(401).send({
                        data:
                            "Unauthorized."
                    })
                } else {
                    let result = await utils.update_user(req.body, decoded);
                    res.status(result[0]).send({
                        data:
                            result[1]
                    });
                }
            } else {
                res.status(401).send({
                    data:
                        "Invalid token."
                }); 
            }
        }
    } else {
        res.status(400).send({
            data:
                "Bad request."
        })
    }
}

exports.upload = async (req, res) => {
    if(req.body.token !== undefined && typeof(req.body.token) === "string") {
        let decoded = utils.verify_jwt(req, req.body.token);
        if(decoded.username) {
            if(req.files.picture !== undefined) {
                let profile_picture_image = req.files.picture;
                let new_uuid = uuidv4();
                let filename = UPLOADS_DIR + new_uuid+'.png';
                profile_picture_image.mv(filename);
                const current_user = await Users.findOne({where: {username: decoded.username}});
                const has_current_pp = await Files.findOne({where: {user_id: current_user.id}});
                if(has_current_pp) {
                    try {
                        fs.unlinkSync(has_current_pp.path);
                        await has_current_pp.destroy();
                    } catch(err) {
                        res.status(500).send({
                            data:
                                "Internal Server Error."
                        });
                        return;
                    }
                }
                const created_file = await Files.create({uuid: new_uuid, path: filename, user_id: current_user.id});
                if(created_file.id === null) {
                    res.status(500).send({
                        data:
                            "Internal Server Error."
                    });
                } else {
                    res.redirect("/profile");
                }
            } else {
                res.status(400).send({
                    data:
                        "Bad request."
                });
            }
        } else {
            res.status(401).send({
                data:
                    "Invalid token."
            });
        }
    } else {
        res.status(400).send({
            data:
                "Bad request."
        });
    }
}