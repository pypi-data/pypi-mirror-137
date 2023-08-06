

import re

_ipv4_regex = "(\\d{1,2}|(0|1)\\d{2}|2[0-4]\\d|25[0-5])"

ipv4_regex = re.compile(
    _ipv4_regex + "\\." + \
    _ipv4_regex + "\\." + \
    _ipv4_regex + "\\." + \
    _ipv4_regex)


def is_ip_address_valid_regex(ip_address: str) -> bool:
    return ipv4_regex.fullmatch(ip_address) != None


name_regex = re.compile("[a-zA-z]+")
username_regex = re.compile("[a-zA-Z0-9_]+")
password_regex = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})")
email_regex = re.compile(r"[a-zA-Z0-9-.]+@[a-zA-Z0-9-.]+")

