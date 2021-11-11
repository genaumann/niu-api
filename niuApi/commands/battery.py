import niuApi.apicommands as apicommands

def list(serial: str = None, print: list = ['bmsId'], **kwargs) -> dict:
    """Lists Batteries connected to the scooter

    Args:
        serial (str, optional): serial number of scooter. Defaults to None.
        print (list, optional): Set the options to print. Defaults to ['bmsId'].

    Returns:
        dict: key: serial number, values: batteries with subkeys and subvalues
    """

    possible_prints = ['bmsId']

    scooters = apicommands.v5.scooter_list()

    out = {}
    battery_info = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        
        if serial is not None:
            if sn != serial:
                continue
        
        batteries = apicommands.v3.motor_data_battery_info(sn).get('batteries')
        for values in batteries.values():
            bmsid = values.get('bmsId')
            battery_info[bmsid] = {}

            for arg in print:
                try:
                    if arg in possible_prints: battery_info[bmsid][arg] = values[arg]
                except KeyError:
                    pass
            
    out[sn] = battery_info

    return out