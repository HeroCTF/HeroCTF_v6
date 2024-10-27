const db = require("../models");
const Complains = db.Complains;
const utils = require("../utils");

exports.getAll = async (req, res) => {
    let decoded = utils.verify_jwt(req);
    if(decoded.username) {
        res.status(200).send(await Complains.findAll());
    } else {
        res.status(401).send({
            data:
                "Invalid token."
        });
    }
}