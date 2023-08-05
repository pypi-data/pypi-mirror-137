from ...util import registry

@registry.keyboards("en_qwerty.v1")
def create_qwerty_en():
    qwerty_en = {
        "default": [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
        ],
        "shift": [
            ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", '"'],
            ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"],
        ],
    }
    return qwerty_en