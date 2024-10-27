module.exports = (sequelize, DataTypes) => {
    const Users = sequelize.define("users", {
      id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      username: {
        type: DataTypes.STRING
      },
      password: {
        type: DataTypes.STRING
      },
      firstname: {
        type: DataTypes.STRING
      },
      lastname: {
        type: DataTypes.STRING
      }
    }, 
    {
      timestamps: false,
      updatedAt: false,
      createdAt: false
    });
  
    return Users;
};