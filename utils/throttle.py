from rest_framework.throttling import UserRateThrottle


class SearchThrottle(UserRateThrottle):
    rate = '200/min'


class UpdateThrottle(UserRateThrottle):
    rate = '6/min'