from copy import deepcopy

from maintain_ner_position.my_utils import check_entity_position, \
    convert_entity_object_type, reconvert_entity_object_type


def delete_sub_content(content, entity_list, start, end, keep_sub_entity=True):
    """
    删除部分文本，并保持对应的实体列表的索引正确

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param start: 待删除片段的起始索引，删除时该索引按照左闭右开使用，即实际删除的片段为：[start, end)
    :param end: 待删除片段的终止索引，删除时该索引按照左闭右开使用，即实际删除的片段为：[start, end)
    :param keep_sub_entity: 是否保留被删除了一部分的实体，默认值为True
    :return:
    """
    if start == end:
        return content, entity_list

    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    check_entity_position(content, entity_list)
    if not start < end:
        raise RuntimeError(f"待删除片段的起始索引位置必须小于终止索引位置，输入索引不满足该条件，起始索引：{start}，终止索引：{end}")
    if start < 0 or end < 0 or start >= len(content) or end > len(content):
        raise RuntimeError(f"待删除片段的起止索引不合法，请检查其是否满足条件：start < 0 or end < 0 or start >= len(content) or end > len(content)")

    new_content = content[:start] + content[end:]

    new_entity_list = []
    for e in entity_list:
        if e["end"] <= start:  # 情况1：实体 e 在被删除的片段左侧；策略：不用动；
            new_entity_list.append(e)
            continue

        if e["start"] < start < e["end"] <= end:  # 情况2：实体 e 的后面部分与被删除片段重叠；策略：删除实体 e 的后面部分；
            if keep_sub_entity:
                e["end"] = start
                new_entity_list.append(e)
            continue

        if start <= e["start"] and e["end"] <= end:  # 情况3：实体 e 整个包含在被删除片段中；策略：删除整个实体 e；
            continue

        if e["start"] < start and end < e["end"]:  # 情况4：实体 e 中间部分是被删除的片段；策略：删除实体 e 的中间部分，两头部分保留，这里其实变为了两个实体；
            if keep_sub_entity:
                e_left = deepcopy(e)
                e_left["en"] = start
                new_entity_list.append(e_left)

                e_right = deepcopy(e)
                e_right["start"] = end
                e_right["start"] -= (end - start)  # 起止位置都向左偏移
                e_right["end"] -= (end - start)  # 起止位置都向左偏移
                new_entity_list.append(e_right)
            continue

        if start <= e["start"] < end < e["end"]:  # 情况5：实体 e 的前面部分与被删除片段重叠；策略：删除实体 e 的前面部分；
            if keep_sub_entity:
                e["start"] = end
                e["start"] -= (end - start)  # 起止位置都向左偏移
                e["end"] -= (end - start)  # 起止位置都向左偏移
                new_entity_list.append(e)
            continue

        if end <= e["start"]:  # 情况6：实体 e 在被删除片段右侧；策略：索引都向左偏移一下；
            e["start"] -= (end - start)  # 起止位置都向左偏移
            e["end"] -= (end - start)  # 起止位置都向左偏移
            new_entity_list.append(e)
            continue

    for e in new_entity_list:
        e["value"] = new_content[e["start"]:e["end"]]
    # 对所有实体进行去重
    new_entity_list = list({(e["start"], e["end"], e["type"]): e for e in new_entity_list}.values())

    new_entity_list = reconvert_entity_object_type(new_entity_list, entity_object_type)
    return new_content, new_entity_list


def delete_entity_with_idx(content, entity_list, entity_idx, keep_sub_entity=True):
    """
    删除指定实体对应的文本

    :param content: 原始文本
    :param entity_list: 原始文本对应的实体列表
    :param entity_idx: 待删除的实体在实体列表中的索引
    :param keep_sub_entity: 是否保留被删除了一部分的实体，默认值为True
    :return:
    """
    entity_list, entity_object_type = convert_entity_object_type(entity_list)
    if entity_idx >= len(entity_list):
        raise RuntimeError(f"要删除的实体索引越界, entity_idx: {entity_idx}, entity list length: {len(entity_list)}")

    entity = entity_list[entity_idx]
    start, end = entity["start"], entity["end"]
    new_content, new_entity_list = delete_sub_content(content, entity_list, start, end, keep_sub_entity)

    new_entity_list = reconvert_entity_object_type(new_entity_list, entity_object_type)
    return new_content, new_entity_list
