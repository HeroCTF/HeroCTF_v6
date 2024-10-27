const Sequelize = require("sequelize");
const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: "/app/database.sqlite",
  operatorsAliases: false
});
const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.Files = require("./files.model.js")(sequelize, Sequelize);
db.Users = require("./users.model.js")(sequelize, Sequelize);
db.Complains = require("./complains.model.js")(sequelize, Sequelize);

module.exports = db;
