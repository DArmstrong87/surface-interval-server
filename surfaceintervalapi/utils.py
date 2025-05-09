CU_FT_TO_LITERS_FACTOR = 28.3168
IMPERIAL_ATM_FACTOR = 33
METRIC_ATM_FACTOR = 10
DEFAULT_TANK_VOLUME = 80


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
    time = dive["time"]
    start_pressure = dive.get("start_pressure")
    end_pressure = dive.get("end_pressure")

    if start_pressure is None or end_pressure is None:
        return None

    print(dive)

    # Default tank volume to 80 Cubic Feet if None
    tank_vol = dive.get("tank_vol", DEFAULT_TANK_VOLUME)  # Cubic feet
    tank_vol = DEFAULT_TANK_VOLUME if tank_vol is None else tank_vol

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
