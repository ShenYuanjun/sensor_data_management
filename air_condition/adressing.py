'''
空调数据总线寻址参数
'''

"发送命令"
# 云盒地址
box_ads = 0x01
# 起始寄存器起始地址
rgs_start = 0x00
# 起始寄存器地址间隔
rgs_len = 0x40
# 数据长度
len_data = 0x08
# 各总线上传感器数（从0开始）
busSensors = [14, 2, 4, 14, 5, 3, 6, 3, 6]

"接受数据"

equipment = ['tank', ]

tank_ref = [['cool_temperature', 1, 1],
            ['cool_temperatue1', 1, 13],
            ['cool_temperatue2', 1, 9],
            ['cool_temperatue3', 1, 7],
            ['cool_temperatue4', 1, 8],
            ['cool_temperatue5', 1, 12],
            ['cool_temperatue6', 1, 14],
            ['heat_level', 1, 2],
            ['heat_temperatue1', 1, 4],
            ['heat_temperatue2', 1, 3],
            ['heat_temperatue3', 1, 5],
            ['heat_temperatue4', 1, 10],
            ['heat_temperatue5', 1, 6],
            ['heat_temperatue6', 1, 11],
            ]

compressor_ref = [['circulating_pump_inlet_pip_temperature', 4, 12],
                  ['circulating_pump_inlet_pip_pressure', 4, 4],
                  ['circulating_pump_return_pip_temperature', 4, 14],
                  ['circulating_pump_return_pip_pressure', 4, 2],
                  ['terminal_water_supply_inlet_pip_temperature', 4, 11],
                  ['terminal_water_supply_inlet_pip_pressure', 4, 1],
                  ['terminal_water_supply_return_pip_temperature', 4, 10],
                  ['terminal_water_supply_return_pip_pressure', 4, 3],
                  ['domestic_hot_water_inlet_pip_temperature', 4, 13],
                  ['domestic_hot_water_inlet_pip_pressure', 4, 5],
                  ]

room1_ref = [['inlet_pip_temperature', 2, 1],
             ['return_pip_temperature', 2, 2],
             ['air_outlet_temperatue', 6, 1],
             ['air_outlet_humidity', 6, 2],
             ['air_outlet_flow_rate', 6, 3],
             ]

room3_ref = [['inlet_pip_temperature', 3, 1],
             ['return_pip_temperature', 3, 2],
             ['air_outlet_temperatue', 7, 1],
             ['air_outlet_humidity', 7, 2],
             ['air_outlet_flow_rate', 7, 3],
             ]

room4_ref = [['inlet_pip_temperature', 3, 3],
             ['return_pip_temperature', 3, 4],
             ['air_outlet_temperatue', 7, 4],
             ['air_outlet_humidity', 7, 5],
             ['air_outlet_flow_rate', 7, 6],
             ]

roomVIP_ref = [['inlet_pip_temperature', 4, 6],
               ['return_pip_temperature', 4, 7],
               ['air_outlet_temperatue', 8, 1],
               ['air_outlet_humidity', 8, 2],
               ['air_outlet_flow_rate', 8, 3],
               ]

conference_front_ref = [['inlet_pip_temperature', 5, 1],
                        ['return_pip_temperature', 5, 2],
                        ['air_outlet_temperatue', 9, 1],
                        ['air_outlet_humidity', 9, 2],
                        ['air_outlet_flow_rate', 9, 3],
                        ]

conference_back_ref = [['inlet_pip_temperature', 5, 3],
                       ['return_pip_temperature', 5, 4],
                       ['air_outlet_temperatue', 6, 4],
                       ['air_outlet_humidity', 6, 5],
                       ['air_outlet_flow_rate', 6, 6],
                       ]

roomControl_ref = [['inlet_pip_temperature', 4, 8],
                   ['return_pip_temperature', 4, 9],
                   ['air_outlet_temperatue', 5, 5],
                   ['air_outlet_humidity', 5, 5],
                   ]

bus1 = [
    ['tank', 'cool_level', 0x81],  # 冷水箱液位
    ['tank', 'heat_level', 0x81],  # 热水箱液位
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.30m处温度
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.15m处温度
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.45m处温度
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.75m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.45m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.60m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.30m处温度
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.60m处温度
    ['tank', 'heat_temperature', 0x01],  # 热水箱0.90m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.75m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.15m处温度
    ['tank', 'cool_temperature', 0x01],  # 冷水箱0.90m处温度
]

bus2 = [
    ['room1', 'inlet_pip_temperature', 0x01],  # 1号房间顶上空调进水管温度
    ['room1', 'return_pip_temperature', 0x01],  # 1号房间顶上空调回水管温度
]

bus3 = [
    ['room3', 'inlet_pip_temperature', 0x01],  # 3号房间顶上空调进水管温度
    ['room3', 'return_pip_temperature', 0x01],  # 3号房间顶上空调回水管温度
    ['room4', 'inlet_pip_temperature', 0x01],  # 4号房间顶上空调进水管温度
    ['room4', 'return_pip_temperature', 0x01],  # 4号房间顶上空调回水管温度
]

bus4 = [
    ['compressor', 'terminal_supply_inlet_pip_pressure', 0x82],  # 末端供水进水管压力
    ['compressor', 'pump_return_pip_pressure', 0x82],  # 设备循环泵回水管压力
    ['compressor', 'terminal_supply_return_pip_pressure', 0x82],  # 末端供水回水管压力
    ['compressor', 'pump_inlet_pip_pressure', 0x82],  # 设备循环泵进水管压力
    ['compressor', 'domestic_hot_water_inlet_pip_pressure', 0x82],  # 生活热水进水管压力
    ['roomVIP', 'inlet_pip_temperature', 0x01],  # vip室顶上空调进水管温度
    ['roomVIP', 'return_pip_temperature', 0x01],  # vip室顶上空调回水管温度
    ['roomControl', 'inlet_pip_temperature', 0x01],  # 调度室顶上空调进水管温度
    ['roomControl', 'return_pip_temperature', 0x01],  # 调度室顶上空调回水管温度
    ['compressor', 'terminal_supply_return_pip_temperature', 0x01],  # 末端供水回水管温度
    ['compressor', 'terminal_supply_inlet_pip_temperature', 0x01],  # 末端供水进水管温度
    ['compressor', 'pump_inlet_pip_temperature', 0x01],  # 设备循环泵进水管温度
    ['compressor', 'domestic_hot_water_inlet_pip_temperature', 0x01],  # 生活热水进水管温度
    ['compressor', 'pump_return_pip_temperature', 0x01],  # 设备循环泵回水管温度
]

bus5 = [
    ['conference_front', 'inlet_pip_temperature', 0x01],  # 会议室前面顶上空调进水管温度
    ['conference_front', 'return_pip_temperature', 0x01],  # 会议室前面顶上空调回水管温度
    ['conference_back', 'inlet_pip_temperature', 0x01],  # 会议室后面顶上空调进水管温度
    ['conference_back', 'return_pip_temperature', 0x01],  # 会议室后面顶上空调回水管温度
    ['roomControl', 'air_outlet_temperature', 0x01, 'air_outlet_humidity', 0x02],  # 调度室顶上空调出风口温湿度
]

bus6 = [
    ['room1', 'air_outlet_temperature', 0x01],  # 1号房间空调出风温度
    ['room1', 'air_outlet_humidity', 0x02],  # 1号房间空调出风湿度
    ['room1', 'air_outlet_flow_rate', 0x30],  # 1号房间空调出风风速
]

bus7 = [
    ['room3', 'air_outlet_temperature', 0x01],  # 3号房间空调出风温度
    ['room3', 'air_outlet_humidity', 0x02],  # 3号房间空调出风湿度
    ['room3', 'air_outlet_flow_rate', 0x30],  # 3号房间空调出风风速
    ['room4', 'air_outlet_temperature', 0x01],  # 4号房间空调出风温度
    ['room4', 'air_outlet_humidity', 0x02],  # 4号房间空调出风湿度
    ['room4', 'air_outlet_flow_rate', 0x30],  # 4号房间空调出风风速
]

bus8 = [
    ['roomVIP', 'air_outlet_temperature', 0x01],  # VIP间空调出风温度
    ['roomVIP', 'air_outlet_humidity', 0x02],  # VIP间空调出风湿度
    ['roomVIP', 'air_outlet_flow_rate', 0x30],  # VIP间空调出风风速
    ['roomControl', 'air_outlet_temperature', 0x01],  # 调度间空调出风温度
    ['roomControl', 'air_outlet_humidity', 0x01],  # 调度间空调出风湿度
]

bus9 = [
    ['conference_front', 'air_outlet_temperature', 0x01],  # 会议室前面空调出风温度
    ['conference_front', 'air_outlet_humidity', 0x02],  # 会议室前面空调出风湿度
    ['conference_front', 'air_outlet_flow_rate', 0x30],  # 会议室前面空调出风风速
    ['conference_back', 'air_outlet_temperature', 0x01],  # 会议室后面空调出风温度
    ['conference_back', 'air_outlet_humidity', 0x02],  # 会议室后面空调出风湿度
    ['conference_back', 'air_outlet_flow_rate', 0x30],  # 会议室后面空调出风风速
]
