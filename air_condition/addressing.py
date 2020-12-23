'''
空调数据总线寻址参数
'''

"发送命令"
# 总线连接地址端口
conn = [
    ['192.168.1.82', 1030],
    ['192.168.1.82', 1031],
    ['192.168.1.82', 1032],
    ['192.168.1.82', 1033],
    ['192.168.1.82', 1034],
    ['192.168.1.82', 1035],
    ['192.168.1.82', 1036],
    ['192.168.1.82', 1037],
    ['192.168.1.82', 1038],
    ['192.168.1.83', 1035],  # 电表
    ['192.168.1.83', 1036]  # 主机
]
# 各总线上传感器数（从0开始）
bus_sensor_number = [14, 2, 4, 14, 5, 3, 6, 3, 6]
# 总线和设备关联（从0开始）
busN = [[0], [1, 5], [2, 6], [3, 4, 7, 8]]
equipmentN = [[0], [1], [2, 3], [4, 5, 6, 7, 8]]

# 云盒地址
box_ads = 0x01
# 起始寄存器起始地址
rgs_start = 0x00
# 起始寄存器地址间隔
rgs_len = 0x40
# 数据长度
len_data = 0x10  # 0x08

# 电流值和物理值转换
i2v = [
    [4, 20],  # 电流范围(mA)
    [-20, 60],  # 温度(℃)
    [0, 100],  # 相对湿度(RH)
    [0, 20],  # 风速(m/s)
]

"接受数据"
# 设备标号
equipment_index = [
    'tank',  # 0
    'room1',  # 1
    'room3',  # 2
    'room4',  # 3
    'compressor',  # 4
    'conference_front',  # 5
    'conference_back',  # 6
    'roomVIP',  # 7
    'roomControl',  # 8
    'meter'  # 9
    'host'  # 10
]

buses = []
# [所属设备号, 变量名, 变量类型]
buses.append([
    [0, 'cool_level', 0x81],  # 冷水箱液位
    [0, 'heat_level', 0x81],  # 热水箱液位
    [0, 'heat_temperature2', 0x01],  # 热水箱0.30m处温度
    [0, 'heat_temperature1', 0x01],  # 热水箱0.15m处温度
    [0, 'heat_temperature3', 0x01],  # 热水箱0.45m处温度
    [0, 'heat_temperature5', 0x01],  # 热水箱0.75m处温度
    [0, 'cool_temperature3', 0x01],  # 冷水箱0.45m处温度
    [0, 'cool_temperature4', 0x01],  # 冷水箱0.60m处温度
    [0, 'cool_temperature2', 0x01],  # 冷水箱0.30m处温度
    [0, 'heat_temperature4', 0x01],  # 热水箱0.60m处温度
    [0, 'heat_temperature6', 0x01],  # 热水箱0.90m处温度
    [0, 'cool_temperature5', 0x01],  # 冷水箱0.75m处温度
    [0, 'cool_temperature1', 0x01],  # 冷水箱0.15m处温度
    [0, 'cool_temperature6', 0x01],  # 冷水箱0.90m处温度
])  # 0

buses.append([
    [1, 'inlet_pip_temperature', 0x01],  # 1号房间顶上空调进水管温度
    [1, 'return_pip_temperature', 0x01],  # 1号房间顶上空调回水管温度
])  # 1

buses.append([
    [2, 'inlet_pip_temperature', 0x01],  # 3号房间顶上空调进水管温度
    [2, 'return_pip_temperature', 0x01],  # 3号房间顶上空调回水管温度
    [3, 'inlet_pip_temperature', 0x01],  # 4号房间顶上空调进水管温度
    [3, 'return_pip_temperature', 0x01],  # 4号房间顶上空调回水管温度
])  # 2

buses.append([
    [4, 'terminal_supply_inlet_pip_pressure', 0x82],  # 末端供水进水管压力
    [4, 'pump_return_pip_pressure', 0x82],  # 设备循环泵回水管压力
    [4, 'terminal_supply_return_pip_pressure', 0x82],  # 末端供水回水管压力
    [4, 'pump_inlet_pip_pressure', 0x82],  # 设备循环泵进水管压力
    [4, 'domestic_hot_water_inlet_pip_pressure', 0x82],  # 生活热水进水管压力
    [7, 'inlet_pip_temperature', 0x01],  # vip室顶上空调进水管温度
    [7, 'return_pip_temperature', 0x01],  # vip室顶上空调回水管温度
    [8, 'inlet_pip_temperature', 0x01],  # 调度室顶上空调进水管温度
    [8, 'return_pip_temperature', 0x01],  # 调度室顶上空调回水管温度
    [4, 'terminal_supply_return_pip_temperature', 0x01],  # 末端供水回水管温度
    [4, 'terminal_supply_inlet_pip_temperature', 0x01],  # 末端供水进水管温度
    [4, 'pump_inlet_pip_temperature', 0x01],  # 设备循环泵进水管温度
    [4, 'domestic_hot_water_inlet_pip_temperature', 0x01],  # 生活热水进水管温度
    [4, 'pump_return_pip_temperature', 0x01],  # 设备循环泵回水管温度
])  # 3

buses.append([
    [5, 'inlet_pip_temperature', 0x01],  # 会议室前面顶上空调进水管温度
    [5, 'return_pip_temperature', 0x01],  # 会议室前面顶上空调回水管温度
    [6, 'inlet_pip_temperature', 0x01],  # 会议室后面顶上空调进水管温度
    [6, 'return_pip_temperature', 0x01],  # 会议室后面顶上空调回水管温度
    [8, 'air_outlet_temperature', 0x01, 'air_outlet_humidity', 0x02],  # 调度室顶上空调出风口温湿度
])  # 4

# [所属设备号, 变量名, 变量类型(i2v)]
buses.append([
    [1, 'air_outlet_temperature', 1],  # 1号房间空调出风温度
    [1, 'air_outlet_humidity', 2],  # 1号房间空调出风湿度
    [1, 'air_outlet_flow_rate', 3],  # 1号房间空调出风风速
])  # 5

buses.append([
    [2, 'air_outlet_temperature', 1],  # 3号房间空调出风温度
    [2, 'air_outlet_humidity', 2],  # 3号房间空调出风湿度
    [2, 'air_outlet_flow_rate', 3],  # 3号房间空调出风风速
    [3, 'air_outlet_temperature', 1],  # 4号房间空调出风温度
    [3, 'air_outlet_humidity', 2],  # 4号房间空调出风湿度
    [3, 'air_outlet_flow_rate', 3],  # 4号房间空调出风风速
])  # 6

buses.append([
    [7, 'air_outlet_temperature', 1],  # VIP间空调出风温度
    [7, 'air_outlet_humidity', 2],  # VIP间空调出风湿度
    [7, 'air_outlet_flow_rate', 3],  # VIP间空调出风风速
    [8, 'air_outlet_temperature', 1],  # 调度间空调出风温度
    [8, 'air_outlet_humidity', 2],  # 调度间空调出风湿度
])  # 7

buses.append([
    [5, 'air_outlet_temperature', 1],  # 会议室前面空调出风温度
    [5, 'air_outlet_humidity', 2],  # 会议室前面空调出风湿度
    [5, 'air_outlet_flow_rate', 3],  # 会议室前面空调出风风速
    [6, 'air_outlet_temperature', 1],  # 会议室后面空调出风温度
    [6, 'air_outlet_humidity', 2],  # 会议室后面空调出风湿度
    [6, 'air_outlet_flow_rate', 3],  # 会议室后面空调出风风速
])  # 8

# [变量名, 寄存器地址, 数据长度]
bus_meter = [
    ['current_combine_total_active_energy', 0x0000, 2],  # 当前组合有功总电能
    ['current_positive_total_active_energy', 0x000A, 2],  # 当前正向有功总电能
    ['current_negative_total_active_energy', 0x0014, 2],  # 当前反向有功总电能
    ['current_total_useless_energy', 0x0186, 2],  # 当前无功总电能
    # ['voltage_A', 0x0300, 1],  # A相电压
    # ['voltage_B', 0x0301, 1],  # B相电压
    # ['voltage_C', 0x0302, 1],  # C相电压
    # ['electric_current_A', 0x0303, 1],  # A相电流
    # ['electric_current_B', 0x0304, 1],  # B相电流
    # ['electric_current_C', 0x0305, 1],  # C相电流
    # ['instant_active_power_A', 0x0306, 1],  # 瞬时A相有功功率
    # ['instant_active_power_B', 0x0307, 1],  # 瞬时B相有功功率
    # ['instant_active_power_C', 0x0308, 1],  # 瞬时C相有功功率
    ['instant_total_active_power', 0x0309, 1],  # 瞬时总有功功率
    # ['instant_useless_power_A', 0x030A, 1],  # 瞬时A相无功功率
    # ['instant_useless_power_B', 0x030B, 1],  # 瞬时B相无功功率
    # ['instant_useless_power_C', 0x030C, 1],  # 瞬时C相无功功率
    ['instant_useless_total_power', 0x030D, 1],  # 瞬时总无功功率
    # ['instant_apparent_power_A', 0x030E, 1],  # 瞬时A相视在功率
    # ['instant_apparent_power_B', 0x030F, 1],  # 瞬时B相视在功率
    # ['instant_apparent_power_C', 0x0310, 1],  # 瞬时C相视在功率
    ['instant_apparent_total_power', 0x0311, 1],  # 瞬时总视在功率
    # ['power_factor_A', 0x0312, 1],  # A相功率因素
    # ['power_factor_B', 0x0313, 1],  # B相功率因素
    # ['power_factor_C', 0x0314, 1],  # C相功率因素
    ['power_factor_total', 0x0315, 1],  # 总功率因素
    ['frequency', 0x0316, 1],  # 频率
]  # 9 meter

# [变量名, 寄存器地址]
# buses.append([
#     ['total_outlet_water_temperature', 101],  # 总出水温度
#     ['equipment_online_status', 102],  # 机组在线状态
#     ['operating_mode', 3005],  # 运行模式
#     ['operating_energy_requirements', 3006],  # 运行能需
#     ['total_outlet_water_temperature_Tw', 3007],  # 总出水温度Tw
#     ['unit_outlet_water_temperature', 3008],  # 单元出水温度
#     ['unit_inlet_water_temperature', 3009],  # 单元进水温度
#     ['condensate_outlet_water_temperature_T3A', 3010],  # 冷凝口出水温度T3A
#     ['condensate_outlet_water_temperature_T3B', 3011],  # 冷凝口出水温度T3B
#     ['outdoor_ambient_temperature', 3012],  # 室外环境温度
#     ['plate_change_inlet_temperature_T6A', 3014],  # 板换进口温度T6A
#     ['plate_change_inlet_temperature_T6B', 3015],  # 板换进口温度T6B
#     ['system_return_air_temperature', 3016],  # 系统回气温度
#     ['T2_refrigerant_liquid_side_temperature', 3017],  # T2冷媒液侧温度
#
# ])  # 10 host

bus_host = [
    ['state_100', 100, 3],
    ['state_3000', 3000, 40],
]

# tank_ref = [['cool_temperature', 1, 1],
#             ['cool_temperatue1', 1, 13],
#             ['cool_temperatue2', 1, 9],
#             ['cool_temperatue3', 1, 7],
#             ['cool_temperatue4', 1, 8],
#             ['cool_temperatue5', 1, 12],
#             ['cool_temperatue6', 1, 14],
#             ['heat_level', 1, 2],
#             ['heat_temperatue1', 1, 4],
#             ['heat_temperatue2', 1, 3],
#             ['heat_temperatue3', 1, 5],
#             ['heat_temperatue4', 1, 10],
#             ['heat_temperatue5', 1, 6],
#             ['heat_temperatue6', 1, 11],
#             ]
#
# compressor_ref = [['circulating_pump_inlet_pip_temperature', 4, 12],
#                   ['circulating_pump_inlet_pip_pressure', 4, 4],
#                   ['circulating_pump_return_pip_temperature', 4, 14],
#                   ['circulating_pump_return_pip_pressure', 4, 2],
#                   ['terminal_water_supply_inlet_pip_temperature', 4, 11],
#                   ['terminal_water_supply_inlet_pip_pressure', 4, 1],
#                   ['terminal_water_supply_return_pip_temperature', 4, 10],
#                   ['terminal_water_supply_return_pip_pressure', 4, 3],
#                   ['domestic_hot_water_inlet_pip_temperature', 4, 13],
#                   ['domestic_hot_water_inlet_pip_pressure', 4, 5],
#                   ]
#
# room1_ref = [['inlet_pip_temperature', 2, 1],
#              ['return_pip_temperature', 2, 2],
#              ['air_outlet_temperatue', 6, 1],
#              ['air_outlet_humidity', 6, 2],
#              ['air_outlet_flow_rate', 6, 3],
#              ]
#
# room3_ref = [['inlet_pip_temperature', 3, 1],
#              ['return_pip_temperature', 3, 2],
#              ['air_outlet_temperatue', 7, 1],
#              ['air_outlet_humidity', 7, 2],
#              ['air_outlet_flow_rate', 7, 3],
#              ]
#
# room4_ref = [['inlet_pip_temperature', 3, 3],
#              ['return_pip_temperature', 3, 4],
#              ['air_outlet_temperatue', 7, 4],
#              ['air_outlet_humidity', 7, 5],
#              ['air_outlet_flow_rate', 7, 6],
#              ]
#
# roomVIP_ref = [['inlet_pip_temperature', 4, 6],
#                ['return_pip_temperature', 4, 7],
#                ['air_outlet_temperatue', 8, 1],
#                ['air_outlet_humidity', 8, 2],
#                ['air_outlet_flow_rate', 8, 3],
#                ]
#
# conference_front_ref = [['inlet_pip_temperature', 5, 1],
#                         ['return_pip_temperature', 5, 2],
#                         ['air_outlet_temperatue', 9, 1],
#                         ['air_outlet_humidity', 9, 2],
#                         ['air_outlet_flow_rate', 9, 3],
#                         ]
#
# conference_back_ref = [['inlet_pip_temperature', 5, 3],
#                        ['return_pip_temperature', 5, 4],
#                        ['air_outlet_temperatue', 6, 4],
#                        ['air_outlet_humidity', 6, 5],
#                        ['air_outlet_flow_rate', 6, 6],
#                        ]
#
# roomControl_ref = [['inlet_pip_temperature', 4, 8],
#                    ['return_pip_temperature', 4, 9],
#                    ['air_outlet_temperatue', 5, 5],
#                    ['air_outlet_humidity', 5, 5],
#                    ]
