from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass(frozen=True)
class AttributeSchema:
    """
    Represents a schema that can be applied to an attribute. Option values are converted to their string
    representations using ``str()`` on them before being sent off in a request.
    """
    attribute_name: str
    data_type: str
    options: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class BloomFilterConfig:
    """
    Represents options to use for entity encoding using bloom filters.
    """
    charset: Optional[str] = None
    hash_strategy: Optional[str] = None
    hash_functions: Optional[int] = None
    filter_size: Optional[int] = None
    token_size: Optional[int] = None
    key: Optional[str] = None


@dataclass(frozen=True)
class Entity:
    """
    Represents an entity that can be encoded using the PPRL encoder service. Attributes are converted to their string
    representations using ``str()`` on them before being sent off in a request.
    """
    identifier: str
    attributes: Dict[str, object]


@dataclass(frozen=True)
class EncodedEntity:
    """
    Represents an encoded entity as a result of the PPRL encoder service.
    """
    identifier: str
    value: str


@dataclass(frozen=True)
class EncoderRequest:
    """
    Represents a request to encode entities with the specified parameters.
    """
    bloom_config: BloomFilterConfig = field(default=BloomFilterConfig("UTF-8", "SHA256", 3, 512, 2))
    schema_list: List[AttributeSchema] = field(default_factory=list)
    entity_list: List[Entity] = field(default_factory=list)
