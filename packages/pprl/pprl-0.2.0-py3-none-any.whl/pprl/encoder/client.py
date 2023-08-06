import urllib.parse
from typing import List

import requests

from .conversion import serialize_encoder_request, deserialize_encoded_entity
from .model import EncoderRequest, EncodedEntity
from ..restutil import prepare_url_for_relative_urljoin, ApiError


def encode_entities(base_url: str, request: EncoderRequest) -> List[EncodedEntity]:
    """
    Encodes the entities contained within the request with the specified encoder configuration.
    Attribute schemas will be added to the request if present.

    :param base_url: URL at which the encoder service is hosted
    :param request: Encoder request
    :return: List of encoded entities
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "encode")
    request = serialize_encoder_request(request)

    r = requests.post(url, json=request)

    # check for 200
    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.bad_request:
            raise ApiError("Invalid encoder parameters", r.status_code)

        raise ApiError("Couldn't encode entities", r.status_code)

    result = r.json()

    if "entities" not in result:
        raise ApiError("Response content is malformed", requests.codes.bad_gateway)

    return [
        deserialize_encoded_entity(e) for e in result["entities"]
    ]


def get_hash_strategies(base_url: str) -> List[str]:
    """
    Returns a list of hash strategies supported by the encoder.

    :param base_url: URL at which the encoder service is hosted
    :return: List of supported hash strategies
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "hash-strategies")

    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        raise ApiError("Couldn't fetch hash strategies", r.status_code)

    return r.json()


class EncoderClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around all encoder client API functions.

        :param base_url: URL at which the encoder service is hosted
        """
        self.__base_url = base_url

    def encode_entities(self, request: EncoderRequest):
        """
        Encodes the entities contained within the request with the specified encoder configuration.
        Attribute schemas will be added to the request if present.

        :param request: Encoder request
        :return: List of encoded entities
        """
        return encode_entities(self.__base_url, request)

    def get_hash_strategies(self):
        """
        Returns a list of hash strategies supported by the encoder.

        :return: List of supported hash strategies
        """
        return get_hash_strategies(self.__base_url)
