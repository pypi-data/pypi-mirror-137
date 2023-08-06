
"""
Data processing methods
"""




def obs_to_dict(observations):
    """Given observations, returns list of dicts
    """

    if not observations or observations == []:
        return []


    if not isinstance(observations, list):
        observations = [observations]




    records = {}

    for o in observations:
        if not o:
            continue

        record_type = o.get('record_type', None)
        record_id = o.get('record_id', None)
        key = o.get('key', None)
        value = o.get('value', None)
        credibility = o.get('credibility', None)
        created_date = o.get('created_date', None)


        if not records.get(record_type, None):
            records[record_type] = {}
        if not records[record_type].get(record_id, None):
            records[record_type][record_id] = {}
            records[record_type][record_id]['@type'] = record_type
            records[record_type][record_id]['@id'] = record_id
            records[record_type][record_id]['credibility'] = credibility
            records[record_type][record_id]['created_date'] = created_date


        if not records[record_type][record_id].get(key, None):
            records[record_type][record_id][key] = []

        if value not in records[record_type][record_id][key]:
            records[record_type][record_id][key].append(value)

    # Transfrom large dict in list
    record_list = []

    for t in records.keys():
        for i in records[t].keys():
            record_list.append(records[t][i])
    
    return record_list



def dict_to_obs(record):
    """Convert dict to observations
    """

    observations = []

    
    if type(record) is list:
        for r in record:
            observations += dict_to_obs(r)
        return observations


    for k in record:

        value = record[k]

        if not isinstance(value, list):
            value = [value]

        for v in value:

            observation = {}
            observation['record_type'] = record.get('@type', None)
            observation['record_id'] = record.get('@id', None)
            observation['key'] = k
            observation['value'] = v
            observation['credibility'] = record.get('credibility', None)
            observation['created_date'] = record.get('created_date', None)

            observations.append(observation)

    return observations
