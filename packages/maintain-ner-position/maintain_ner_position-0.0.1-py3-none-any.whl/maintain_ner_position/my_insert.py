from maintain_ner_position.my_utils import check_entity_position, \
    convert_entity_object_type, reconvert_entity_object_type


def insert_entity(content, entity_list, insert_idx, insert_cont, insert_type):
    """
    插入一个新实体，并维持实体列表中所有的索引值正常；若新插入的文本刚好处于某个实体的边界，新插入的文本不
    会作为实体，原实体保持不变。

    举例如下：
        原文本：小明去招商银行。
        原实体：{"type": "机构", "start": 3, "end": 7, "value": "招商银行"}
        插入文本：中国
        插入索引：3
        新文本：小明去中国招商银行。
        新实体：{"type": "机构", "start": 5, "end": 9, "value": "招商银行"}

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param insert_idx: 插入的位置索引
    :param insert_cont: 待插入的文本
    :param insert_type: 新插入的文本对应的实体类型
    :return:
    """
    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    content, entity_list = insert_content(content, entity_list, insert_idx, insert_cont)

    entity_list.append({
        "type": insert_type,
        "start": insert_idx,
        "end": insert_idx + len(insert_cont),
        "value": content[insert_idx:insert_idx + len(insert_cont)],
    })
    entity_list = reconvert_entity_object_type(entity_list, entity_object_type)
    return content, entity_list


def insert_content(content, entity_list, insert_idx, insert_cont):
    """
    插入一段文本，并维持实体列表中所有的索引值正常；若新插入的文本刚好处于某个实体的边界，新插入的文本不
    会作为实体，原实体保持不变。

    举例如下：
        原文本：小明去招商银行。
        原实体：{"type": "机构", "start": 3, "end": 7, "value": "招商银行"}
        插入文本：中国
        插入索引：3
        新文本：小明去中国招商银行。
        新实体：{"type": "机构", "start": 5, "end": 9, "value": "招商银行"}

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param insert_idx: 插入的位置索引
    :param insert_cont: 待插入的文本
    :return:
    """
    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    check_entity_position(content, entity_list)
    if insert_idx > len(content):
        raise RuntimeError(f"插入的位置索引超过了文本长度，位置索引：{insert_idx}，文本长度：{len(content)}")

    for e in entity_list:
        if e["start"] >= insert_idx:
            e["start"] += len(insert_cont)
        if e["end"] > insert_idx:
            e["end"] += len(insert_cont)

    content = content[:insert_idx] + insert_cont + content[insert_idx:]

    for e in entity_list:
        e["value"] = content[e["start"]:e["end"]]

    entity_list = reconvert_entity_object_type(entity_list, entity_object_type)
    return content, entity_list


def insert_entity_extend_entity(content, entity_list, insert_idx, insert_cont, insert_type):
    """
    插入一个新实体，并维持实体列表中所有的索引值正常；若新插入的文本刚好处于某个实体的边界，会扩展该实体的
    边界，将新插入的文本也作为实体的一部分。

    举例如下：
        原文本：小明去招商银行。
        原实体：{"type": "机构", "start": 3, "end": 7, "value": "招商银行"}
        插入文本：中国
        插入索引：3
        新文本：小明去中国招商银行。
        新实体：{"type": "机构", "start": 3, "end": 9, "value": "中国招商银行"}

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param insert_idx: 插入的位置索引
    :param insert_cont: 待插入的文本
    :param insert_type: 新插入的文本对应的实体类型
    :return:
    """
    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    content, entity_list = insert_content_extend_entity(content, entity_list, insert_idx, insert_cont)

    entity_list.append({
        "type": insert_type,
        "start": insert_idx,
        "end": insert_idx + len(insert_cont),
        "value": content[insert_idx:insert_idx + len(insert_cont)],
    })
    entity_list = reconvert_entity_object_type(entity_list, entity_object_type)
    return content, entity_list


def insert_content_extend_entity(content, entity_list, insert_idx, insert_cont):
    """
    插入一段文本，并维持实体列表中所有的索引值正常；若新插入的文本刚好处于某个实体的边界，会扩展该实体的
    边界，将新插入的文本也作为实体的一部分。

    举例如下：
        原文本：小明去招商银行。
        原实体：{"type": "机构", "start": 3, "end": 7, "value": "招商银行"}
        插入文本：中国
        插入索引：3
        新文本：小明去中国招商银行。
        新实体：{"type": "机构", "start": 3, "end": 9, "value": "中国招商银行"}

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param insert_idx: 插入的位置索引
    :param insert_cont: 待插入的文本
    :return:
    """
    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    check_entity_position(content, entity_list)
    if insert_idx > len(content):
        raise RuntimeError(f"插入的位置索引超过了文本长度，位置索引：{insert_idx}，文本长度：{len(content)}")

    for e in entity_list:
        if e["start"] > insert_idx:
            e["start"] += len(insert_cont)
        if e["end"] >= insert_idx:
            e["end"] += len(insert_cont)

    content = content[:insert_idx] + insert_cont + content[insert_idx:]

    for e in entity_list:
        e["value"] = content[e["start"]:e["end"]]

    entity_list = reconvert_entity_object_type(entity_list, entity_object_type)
    return content, entity_list
