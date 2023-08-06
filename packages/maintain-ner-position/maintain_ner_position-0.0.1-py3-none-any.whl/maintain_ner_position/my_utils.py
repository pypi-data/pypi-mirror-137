from typing import List

ENTITY_OBJECT_TYPE_DICT = 0
ENTITY_OBJECT_TYPE_TUPLE = 1


def check_entity_position(content, entity_list: List[dict]):
    """ 检查输入的实体索引是否都合法 """
    if any([e["start"] < 0 or e["end"] < 0 for e in entity_list]):
        raise RuntimeError(f"实体索引为负, entity list: {entity_list}")
    if not all([e["end"] <= len(content) for e in entity_list]):
        raise RuntimeError(f"实体索引超出文本长度范围, content: {content}, entity list: {entity_list}")
    if not all([e["start"] < e["end"] for e in entity_list]):
        raise RuntimeError(f"存在起始位置不小于终止位置的实体, entity list: {entity_list}")
    if not all([content[e["start"]:e["end"]] == e["value"] for e in entity_list]):
        raise RuntimeError(f"实体的value值与原文本不匹配，content: {content}，entity list: {entity_list}")


def convert_entity_object_type(entity_list):
    if len(entity_list) <= 0:
        return entity_list, ENTITY_OBJECT_TYPE_DICT
    if isinstance(entity_list[0], dict):
        return entity_list, ENTITY_OBJECT_TYPE_DICT
    elif isinstance(entity_list[0], tuple):
        new_entity_list = []
        for e in entity_list:
            start, end, t, value = e[0], e[1], e[2], e[3]
            new_entity_list.append({"start": start, "end": end, "type": t, "value": value})
        return new_entity_list, ENTITY_OBJECT_TYPE_TUPLE
    else:
        raise RuntimeError(f"每个实体的类型仅支持 dict 和 tuple 两种，实际输入的实体类型为：{type(entity_list[0])}")


def reconvert_entity_object_type(entity_list, entity_object_type):
    if entity_object_type == ENTITY_OBJECT_TYPE_TUPLE:
        entity_list = [(e["start"], e["end"], e["type"], e["value"]) for e in entity_list]
    return entity_list
