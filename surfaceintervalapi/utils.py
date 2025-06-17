from decimal import Decimal, ROUND_HALF_UP
from django.core.cache import cache

CU_FT_TO_LITERS_FACTOR = 28.3168
IMPERIAL_ATM_FACTOR = 33
METRIC_ATM_FACTOR = 10
DEFAULT_TANK_VOLUME = 80


def get_rounded_value(value: float, precision: str) -> float:
    decimal_value = Decimal(value)
    rounded_value = decimal_value.quantize(Decimal(precision), rounding=ROUND_HALF_UP)
    return float(rounded_value)


def get_air_consumption_cu_ft_min(dive: dict, units: str):
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
    rounded_value = get_rounded_value(surface_air_consumption_rate, "0.01")
    return float(rounded_value)


def get_air_consumption_ltrs_min(avg_air_consumption_cu_ft_min):
    ltrs_min = avg_air_consumption_cu_ft_min * CU_FT_TO_LITERS_FACTOR
    rounded_value = get_rounded_value(ltrs_min, "0.01")
    return rounded_value


def get_dive_air_consumption(dive: dict, units: str) -> dict:
    dive_cu_ft_min = get_air_consumption_cu_ft_min(dive, units)
    dive_ltrs_min = get_air_consumption_ltrs_min(dive_cu_ft_min)
    return {"cu_ft_min": dive_cu_ft_min, "ltrs_min": dive_ltrs_min}


def get_average_air_consumption(dives: list) -> dict:
    avg_air_consumption_cu_ft_min = sum([d["air_consumption"] for d in dives]) / len(dives)
    rounded_avg_air_consumption_cu_ft_min = get_rounded_value(avg_air_consumption_cu_ft_min, "0.01")
    rounded_avg_air_consumption_ltrs_min = get_air_consumption_ltrs_min(
        avg_air_consumption_cu_ft_min
    )
    return {
        "cu_ft_min": rounded_avg_air_consumption_cu_ft_min,
        "ltrs_min": rounded_avg_air_consumption_ltrs_min,
    }


def get_values_from_cache(key: str) -> dict:
    try:
        values = cache.get(key)
        if values is not None:
            print(f"Returning '{key}' values from cache.")
        return values
    except Exception as ex:
        print(f"Exception getting cache values key: {key}, exception: {ex}")
        return None


def cache_values(key: str, data, timeout_min: int):
    try:
        cache.set(key, data, timeout_min * 60)
        print(f"Caching values '{key}'")
    except Exception as ex:
        print(f"Unable to set cache key {key}: {ex}")


def invalidate_cache(key: str):
    try:
        cache.delete(key)
        print(f"Deleting cache key '{key}'")
    except Exception as ex:
        print(f"Unable to invalidate cache key {key}: {ex}")


def invalidate_multiple_cache_keys(keys: list):
    try:
        for key in keys:
            cache.delete(key)
            print(f"Invalidating cache key '{key}'")
    except Exception as ex:
        print(f"Unable to invalidate cache keys {keys}: {ex}")


def get_cache_key(user_id: int, model: str, pk: int = None):
    pk = "" if pk is None else f":{pk}"
    return f"user:{user_id}:{model}{pk}"
