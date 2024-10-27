module.exports = (sequelize, DataTypes) => {
    const Complains = sequelize.define("complains", {
      id: {
        type: DataTypes.STRING,
        primaryKey: true
      },
      reason: {
        type: DataTypes.STRING
      },
      file_id: {
        type: DataTypes.STRING
      }
    }, 
    {
      timestamps: false,
      updatedAt: false,
      createdAt: false
    });
  
    return Complains;
};