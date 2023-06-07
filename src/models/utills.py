def is_smart_tv(user_agent_string):
    smart_tv_keywords = ["SMART-TV", "TV"]
    smart_tv_substrings = ["Tizen", "webOS", "NetCast"]
    user_agent = user_agent_string.upper()
    is_smart_tv = any(keyword in user_agent for keyword in smart_tv_keywords)
    is_smart_tv |= any(substring in user_agent for substring in smart_tv_substrings)
    return is_smart_tv
