import math
from math import radians


class ShynaDistanceDifference:
    """"
    Return the distance difference in km based on latitude and longitude

    Method is:
    def get_distance_difference(default_latitude, default_longitude, new_latitude, new_longitude): returns float value
    """
    R = 6371.0

    def get_distance_difference(self, default_latitude, default_longitude, new_latitude, new_longitude):
        lat1 = radians(default_latitude)
        lon1 = radians(default_longitude)
        lat2 = radians(new_latitude)
        lon2 = radians(new_longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.R * c
        return float(distance)
