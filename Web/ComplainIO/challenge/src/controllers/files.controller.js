const db = require("../models");
const utils = require("../utils");
const fs = require("fs");
const carbone = require('carbone');
const Files = db.Files;
const Users = db.Users;

exports.createTemplate = async (req, res) => {
    let decoded = utils.verify_jwt(req);
    if(decoded.username) {
        if(req.body.uuid && req.body.id && typeof(req.body.uuid) === "string" && typeof(req.body.id) == "number") {
            const file = await Files.findOne({where: {uuid: req.body.uuid}});
            let current_user = await Users.findOne({where: {username: decoded.username}});
            if(current_user.id != req.body.id) {
                res.status(401).send({
                    data:
                        "Unauthorized."
                });
            } else {
                if(req.body.firstname !== current_user.firstname || req.body.lastname !== current_user.lastname) {
                    await utils.update_user(req.body, decoded);
                    current_user = await Users.findOne({where: {username: decoded.username}});
                }
                if(file.uuid) {
                    var data = {
                        firstname: current_user.firstname,
                        lastname: current_user.lastname
                    };
                    carbone.render(file.path, data, function(err, result){
                        if (err) {
                            res.status(500).send({
                                data:
                                    "Internal Server Error."
                            });
                        } else {
                            res.status(200).send({
                                data:
                                    result.toString('base64')
                            });
                        }
                    });
                } else {
                    res.status(404).send({
                        data:
                            "File not found."
                    });
                }
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
}

exports.getProfilePicture = async (req, res) => {
    if(req.query.token !== undefined && typeof(req.query.token) === "string") {
        let decoded = utils.verify_jwt(req, req.query.token);
        if(decoded.username) {
            if(req.params.uuid && typeof(req.params.uuid) === "string") {
                const file = await Files.findOne({where: {uuid: req.params.uuid}});
                if(file && file.uuid) {
                    const current_user = await Users.findOne({where: {username: decoded.username}});
                    if(file.user_id === current_user.id) {
                        try {
                            var s = fs.createReadStream(file.path);
                            s.on('open', function() {
                                res.set('Content-Type', 'image/png');
                                s.pipe(res);
                            });
                            s.on('error', function() {
                                res.set('Content-Type', 'text/plain');
                                res.status(500).end('Internal Server Error');
                            })
                        } catch(err) {
                            res.status(500).send({
                                data:
                                    "Internal Server Error."
                            });
                        }
                    } else {
                        res.status(401).send({
                            data:
                                "Unauthorized."
                        });
                    }
                } else {
                    res.status(404).send({
                        data:
                            "File not found."
                    });
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