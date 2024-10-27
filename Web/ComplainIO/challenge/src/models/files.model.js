module.exports = (sequelize, DataTypes) => {
    const Files = sequelize.define("files", {
      uuid: {
        type: DataTypes.STRING,
        primaryKey: true
      },
      path: {
        type: DataTypes.STRING
      },
      user_id: {
        type: DataTypes.INTEGER,
        allowNull: true,
        references: 'users',
        referencesKey: 'id'
      }
    }, 
    {
      timestamps: false,
      updatedAt: false,
      createdAt: false
    });
  
    return Files;
};