let jwt = require('jsonwebtoken');
const secret_key = process.env.SECRET_KEY || "hero";
const db = require("../models");
const Users = db.Users;
const FORBIDDEN_MODIFIED = ["id","username","password"];
const all_fields = FORBIDDEN_MODIFIED.concat(["firstname","lastname"]);

const merge = (obj1, obj2) => {
    for (let key of Object.keys(obj2)) {
      const val = obj2[key];
      if(FORBIDDEN_MODIFIED.includes(key)) {
        continue
      }
      if (typeof obj1[key] !== "undefined" && typeof val === "object") {
        obj1[key] = merge(obj1[key], val);
      } else {
        obj1[key] = val;
      }
    }
  
    return obj1;
  };

exports.verify_jwt = (req, user_token=null) => {
    let decoded = {};
    let token = "";
    if(req.headers.authorization !== undefined) {
        let parts = req.headers.authorization.split("Bearer ")
        if(parts.length == 2) {
            token = parts[1];
        }
    }
    if(user_token !== null) {
        token = user_token;
    }
    try {
        decoded = jwt.verify(token, secret_key);
    } catch(err) {}
    return decoded;
}

exports.sign_jwt = (data) => {
    return jwt.sign(data, secret_key)
}

exports.update_user = async (data, _) => {
    const user_id = data.id;
    let current_user = await Users.findByPk(user_id);
    if(!current_user) {
        return [404, "User not found."];
    }
    let user_database_content = {};
    let incoming_user_updates = data;
    for(var i=0; i<all_fields.length; i++) {
        user_database_content[all_fields[i]] = current_user[all_fields[i]];
    }
    merge(user_database_content, incoming_user_updates);
    const num = await Users.update(user_database_content, {
        where: {id: user_id}
    })
    if(num == 1) {
        return [200,"User updated."];
    } else {
        return [500,"Internal server error."];
    }
}