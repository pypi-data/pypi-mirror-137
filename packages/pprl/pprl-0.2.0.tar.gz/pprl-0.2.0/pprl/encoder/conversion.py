from typing import List, Dict

from .model import Entity, EncoderRequest, AttributeSchema, EncodedEntity, BloomFilterConfig


def serialize_entity(entity: Entity) -> Dict:
    """
    Converts an entity into a dictionary.

    :param entity: Entity to convert
    :return: Converted entity
    """
    d = {"id": entity.identifier}
    d.update({
        k: str(v) for k, v in entity.attributes.items()
    })

    return d


def serialize_entities(entity_list: List[Entity]) -> List[Dict]:
    """
    Converts an list of entities into a list of dictionaries.

    :param entity_list: Entities to convert
    :return: List of converted entities
    """
    return [
        serialize_entity(entity) for entity in entity_list
    ]


def serialize_schema(schema: AttributeSchema) -> Dict:
    """
    Converts an attribute schema into a dictionary.

    :param schema: Attribute schema to convert
    :return: Converted attribute schema
    """
    d = {
        "attributeName": schema.attribute_name,
        "dataType": schema.data_type
    }

    d.update({
        k: str(v) for k, v in schema.options.items()
    })

    return d


def serialize_schemas(schema_list: List[AttributeSchema]) -> List[Dict]:
    """
    Converts a list of attribute schemas into a dictionary.

    :param schema_list: Attribute schemas to convert
    :return: List of converted attribute schemas
    """
    return [
        serialize_schema(schema) for schema in schema_list
    ]


def serialize_bloom_filter_config(config: BloomFilterConfig) -> Dict:
    """
    Converts a bloom filter config object into a dictionary.

    :param config: Config to convert
    :return: Converted config
    """
    d = {}

    if config.charset is not None:
        d["charset"] = config.charset

    if config.hash_strategy is not None:
        d["hashStrategy"] = config.hash_strategy

    if config.hash_functions is not None:
        d["hashFunctions"] = config.hash_functions

    if config.filter_size is not None:
        d["filterSize"] = config.filter_size

    if config.token_size is not None:
        d["tokenSize"] = config.token_size

    if config.key is not None:
        d["key"] = config.key

    return d


def serialize_encoder_request(request: EncoderRequest) -> Dict:
    """
    Converts an encoder request object into a dictionary.

    :param request: Encoder request to convert
    :return: Converted encoder request
    """
    if len(request.entity_list) == 0:
        return {}

    return {
        "bloomFilter": serialize_bloom_filter_config(request.bloom_config),
        "entities": serialize_entities(request.entity_list),
        "schemas": serialize_schemas(list(request.schema_list))
    }


def deserialize_encoded_entity(d: Dict) -> EncodedEntity:
    """
    Converts a dictionary into an encoded entity.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return EncodedEntity(d["id"], d["value"])
