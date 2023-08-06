import math


def saturated(lt: float) -> float:
    """
    Calculate the Saturated Vapor Pressure.

    Parameters
    ----------
    lt : float
        Leaf Temperature

    Returns
    -------
    vp_sat
    """
    return (610.78 * math.pow(10, (lt * 7.5) / (lt + 237.3))) / 1000


def air(at: float, rh: float) -> float:
    """
    Calculate the Air Vapor Pressure.

    Parameters
    ----------
    at : float
        Air Temperature
    rh : float
        Relative Humidity

    Returns
    -------
    vp_air
    """
    return saturated(at) * (rh / 100)


def deficit(lt: float, at: float, rh: float) -> float:
    """
    Calculate the Vapor Pressure Deficit.

    Parameters
    ----------
    lt : float
        Leaf Temperature
    at : float
        Air Temperature
    rh : float
        Relative Humidity

    Returns
    -------
    vp_def
    """
    return saturated(lt) - air(at, rh)
