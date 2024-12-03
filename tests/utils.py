import re


def clean_stdout_content(raw_info: str) -> str:
    """
    Clean human-readable raw stdout message from all formatting characters
    and leave only letters and spaces
    :param raw_info: stdout content
    :return: cleaned stdout content
    """
    clean_output = re.sub("[^\w.]", " ", raw_info)
    clean_output = re.sub("\s+", " ", clean_output)
    return clean_output
