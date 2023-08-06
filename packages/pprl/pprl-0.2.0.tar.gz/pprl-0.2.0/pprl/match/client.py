import urllib.parse
from typing import List

import requests

from .conversion import serialize_match_request, deserialize_match
from .model import MatchRequest, Match
from ..restutil import prepare_url_for_relative_urljoin, ApiError


def match_bit_vectors(base_url: str, request: MatchRequest) -> List[Match]:
    """
    Matches the bit vectors contained within the request.

    :param base_url: URL at which the match service is hosted
    :param request: Match request
    :return: List of matched entities
    """
    if len(request.domain) == 0 or len(request.range) == 0:
        raise []

    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "match")
    r = requests.post(url, json=serialize_match_request(request))

    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.bad_request:
            raise ApiError("Invalid match parameters", r.status_code)

        raise ApiError("Couldn't match entities", r.status_code)

    result = r.json()

    return [
        deserialize_match(m) for m in result["correspondences"]
    ]


def get_match_methods(base_url: str) -> List[str]:
    """
    Returns the match methods supported by the matcher.

    :param base_url: URL at which the match service is hosted
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "match-methods")
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        raise ApiError("Couldn't fetch match methods", r.status_code)

    return r.json()


def get_match_modes(base_url: str) -> List[str]:
    """
    Returns the match modes supported by the matcher.

    :param base_url: URL at which the match service is hosted
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "match-modes")
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        raise ApiError("Couldn't fetch match methods", r.status_code)

    return r.json()


def get_selection_strategies(base_url: str) -> List[str]:
    """
    Returns the selection strategies supported by the matcher.

    :param base_url: URL at which the match service is hosted
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "selection-strategies")
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        raise ApiError("Couldn't fetch match methods", r.status_code)

    return r.json()


class MatchClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around all match client API functions.

        :param base_url: URL at which the match service is hosted
        """
        self.__base_url = base_url

    def match_bit_vectors(self, request: MatchRequest) -> List[Match]:
        """
        Matches the bit vectors contained within the request.

        :param request: Match request
        :return: List of matched entities
        """
        return match_bit_vectors(self.__base_url, request)

    def get_match_methods(self) -> List[str]:
        """
        Returns the match methods supported by the matcher.
        """
        return get_match_methods(self.__base_url)

    def get_match_modes(self) -> List[str]:
        """
        Returns the match modes supported by the matcher.
        """
        return get_match_modes(self.__base_url)

    def get_selection_strategies(self) -> List[str]:
        """
        Returns the selection strategies supported by the matcher.
        """
        return get_selection_strategies(self.__base_url)