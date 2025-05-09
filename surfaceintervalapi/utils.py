CU_FT_TO_LITERS_FACTOR = 28.3168
IMPERIAL_ATM_FACTOR = 33
METRIC_ATM_FACTOR = 10


def get_air_consumption_cu_ft_min(dive, units):
    """
    Calculates surface air consumption rate
    0.315 cubic feet per minute
    Multiply by 28.3168 to get liters per minute

    This will always be an over-estimation as it is calculated
    based on the deepest depth.
    Truer SAC rate is based on average depth of the dive.
    """

    depth = dive["depth"]
    start_pressure = dive["start_pressure"]
    time = dive["time"]
    end_pressure = dive["end_pressure"]
    tank_vol = dive["tank_vol"]  # Cubic feet

    atm = IMPERIAL_ATM_FACTOR if units.lower() == "imperial" else METRIC_ATM_FACTOR
    bar_atm = (depth / atm) + 1
    psi_consumed = start_pressure - end_pressure

    working_pressure = start_pressure
    cubic_feet_consumed_air = (tank_vol * psi_consumed) / working_pressure
    surface_air_consumption_rate = cubic_feet_consumed_air / time / bar_atm

    # liters_per_minute = round(surface_air_consumption_rate * 28.3168, 3)
    # print(f"Consumption rate is {liters_per_minute} liters per minute")
    return round(surface_air_consumption_rate, 3)


def get_air_consumption_ltrs_min(avg_air_consumption_cu_ft_min):
    return round(avg_air_consumption_cu_ft_min * CU_FT_TO_LITERS_FACTOR, 3)
