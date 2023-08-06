from typing import Dict

from .model import MatchConfig, MatchRequest, Match


def serialize_match_config(config: MatchConfig) -> Dict:
    """
    Converts a match configuration object into a dictionary.

    :param config: Match configuration to convert
    :return: Converted match configuration
    """
    d = {}

    if config.match_function is not None:
        d["matchFunction"] = config.match_function

    if config.selection_strategy is not None:
        d["selectionStrategy"] = config.selection_strategy

    if config.threshold is not None:
        d["threshold"] = config.threshold

    if config.match_mode is not None:
        d["matchMode"] = config.match_mode

    return d


def serialize_match_request(request: MatchRequest) -> Dict:
    """
    Converts a match request into a dictionary.

    :param request: Match request object to convert
    :return: Converted match request
    """
    return {
        "domain": request.domain,
        "range": request.range,
        "config": serialize_match_config(request.match_config),
    }


def deserialize_match(d: Dict) -> Match:
    """
    Converts a match dictionary into a match object.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return Match(
        domain_vector=d["domain"],
        range_vector=d["range"],
        confidence=d["confidence"]
    )
