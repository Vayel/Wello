import signalslot

configuration = signalslot.Signal(args=['config'])

pump_in_state = signalslot.Signal(args=['running'])
command_pump_in = signalslot.Signal(args=['running'])

update_water_volume = signalslot.Signal(args=['volume'])
water_volume_updated = signalslot.Signal(args=['volume'])
