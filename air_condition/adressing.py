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

"接受数据"

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

main_ref = [['circulating_pump_inlet_pip_temperature', 4, 12],
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
