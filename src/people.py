PEOPLE = {
    "Королева": "https://portal.kraftway.lan/default.asp?p_no=54910&subtmpl=people_info&back_url=",
    "Папа":     "https://portal.kraftway.lan/default.asp?p_no=55862&subtmpl=people_info&back_url=",
    "Лупа":     "https://portal.kraftway.lan/default.asp?p_no=56221&subtmpl=people_info&back_url=",
    "Пупа":     "https://portal.kraftway.lan/default.asp?p_no=56655&subtmpl=people_info&back_url=",
    "Лиза":     "https://portal.kraftway.lan/default.asp?p_no=56853&subtmpl=people_info&back_url=",
    "Олег":     "https://portal.kraftway.lan/default.asp?p_no=54947&subtmpl=people_info&back_url=",
    "Отладов":  "https://portal.kraftway.lan/default.asp?p_no=56224&subtmpl=people_info&back_url=",
    "Андрей": "https://portal.kraftway.lan/default.asp?ob_no=&subtmpl=people_info&p_no=56852"
}


def color_word(is_green: bool) -> str:
    return "зелён" if is_green else "красн"


def lingvist(name: str, base_color: str):
    fem_names = {"Лиза", "Королева"}
    stal = "а" if name in fem_names else ""
    col_end = "ой" if name in fem_names else "ым"
    status = "на месте" if base_color == "зелён" else "отсутствует"
    return stal, col_end, status


def became_phrase(name: str, is_green: bool) -> str:
    base = color_word(is_green)
    stal, col_end, _ = lingvist(name, base)
    return f"{name} стал{stal} {base}{col_end}."
