ssh root@192.168.1.10
dell123456


conn = new Mongo();
db = conn.getDB("admin");
db.auth("myUserAdmin", "123456");

db.createUser(
    {
      user: "sensorManager",
      pwd: "manage123456",
      roles: [ { role: "readWrite", db: "sensor_management" }]
    }
  )

  db.createUser(
    {
      user: "sensorTester",
      pwd: "test123456",
      roles: [ { role: "read", db: "sensor_management" }]
    }
  )



  collections = ['Cross-references', 'AirConditioner', 'Environment', 'Log']

Cross-references: {
    index: String,
    room: Number,
    level: Number,
    number: Number
}

Environment: {
    index: String,
    two_in_one: {
        teperature: Number,
        Humidity: Number
    },
    six_in_one: {
        temperature: Number,
        humidity: Number,
        CO2: Number,
        pm25: Number,
        pm1: Number,
        pm10: Number
    },
    time: DataTime
}

AirConditioner: {
    tank: {
        c_level: Number,
        cool_temperatue1: Number,
        cool_temperatue2: Number,
        cool_temperatue3: Number,
        cool_temperatue4: Number,
        cool_temperatue5: Number,
        cool_temperatue6: Number,
        h_level: Number,
        heat_temperatue1: Number,
        heat_temperatue2: Number,
        heat_temperatue3: Number,
        heat_temperatue4: Number,
        heat_temperatue5: Number,
        heat_temperatue6: Number,
    },
    device: {
        pump_inlet_tem: Number,
        circulating_pump_inlet_pip_pre: Number,
        circulating_pump_return_pip_temperatue: Number,
        circulating_pump_return_pip_pressure: Number,
        water_supply_inlet_tem: Number,
        terminal_water_supply_inlet_pip_pressure: Number,
        terminal_water_supply_return_pip_temperatue: Number,
        terminal_water_supply_return_pip_pressure: Number,
        domestic_hot_water_inlet_pip_temperatue: Number,
        domestic_hot_water_inlet_pip_pressure: Number
    },
    terminal_room1: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_tem: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_room3: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_room4: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_roomConference_front: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_roomConference_back: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_roomVIP: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    terminal_roomSchedule: {
        inlet_pip_temperature: Number,
        return_pip_temperature: Number,
        air_outlet_temperatue: Number,
        air_outlet_humidity: Number,
        air_outlet_flow_rate: Number
    },
    time: DataTime
}

log: {
    description: String,
    time: DateTime
}