__version__ = "0.0.2"

from .my_insert import insert_content, insert_content_extend_entity, insert_entity, insert_entity_extend_entity
from .my_delete import delete_sub_content, delete_entity_with_idx

__all__ = (
    "__version__",
    "insert_content",
    "insert_content_extend_entity",
    "insert_entity",
    "insert_entity_extend_entity",
    "delete_sub_content",
    "delete_entity_with_idx",
)
