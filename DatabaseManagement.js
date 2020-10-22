conn = new Mongo();
db = conn.getDB("admin");
db.auth("myUserAdmin", "123456");

db.createUser(
    {
      user: "sensorManager",
      pwd: "manage123456",
      roles: [ { role: "readWrite", db: "sensor" }]
    }
  )

  db.createUser(
    {
      user: "sensorTester",
      pwd: "test123456",
      roles: [ { role: "read", db: "sensor" }]
    }
  )