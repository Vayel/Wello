import signalslot

configuration = signalslot.Signal(args=['config'])

pump_in_state = signalslot.Signal(args=['running'])
command_pump_in = signalslot.Signal(args=['running'])

urban_network_state = signalslot.Signal(args=['running'])
command_urban_network = signalslot.Signal(args=['running'])

update_water_volume = signalslot.Signal(args=['volume'])
water_volume_updated = signalslot.Signal(args=['volume'])

update_water_flow_in = signalslot.Signal(args=['value'])
water_flow_in_updated = signalslot.Signal(args=['value'])

update_water_flow_out = signalslot.Signal(args=['value'])
water_flow_out_updated = signalslot.Signal(args=['value'])
