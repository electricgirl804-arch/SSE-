import numpy as np

def calc_panels(load_kwh, ghi=5.5, pr=0.75):
    return round(load_kwh / (ghi * pr * 0.55), 0)

def calc_string(volt, panels, temp=45):
    voc_max = volt * panels * 1.25
    return round(voc_max, 2)

def calc_cable(length, current, volt=400, vd=2):
    area = (2 * length * current) / (56 * volt * (vd/100))
    return round(area, 2)

def calc_battery_runtime(kwh, watt, dod=0.8, eff=0.95):
    usable = kwh * 1000 * dod * eff
    hours = usable / watt
    return round(hours, 1)
