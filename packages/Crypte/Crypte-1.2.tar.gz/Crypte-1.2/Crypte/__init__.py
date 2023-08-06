Keys = ["\n", "a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "²",  "d", "f", "g", "h", "j", "k", "l", "m", "w", "x", "c", "v", "b", "n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "é", "à", "è", " ", "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "W", "X", "C", "V", "B", "N", "?", ",", ";", ".", ":", "/", "!", ")", "(", "^", "'", "+", "-", "=", "[", "]", "{", "}", "ê", "¨", "@", "-", ",", "/", "'", "<", ">", "_", "-", "~", "#", "|", "ç", "*", "&", "°"]


def init_keys(keys):
    for k in keys:
        Keys.append(k)
    return print(f"Clés {keys} ajoutée(s) !")

def decrypte(msg):
    New_Message = ""

    m = msg.split(".")
    for Number in m:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            pass
    New_Message = New_Message.replace(",", "")
    return New_Message


def crypte_with_file(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            rd = f.read()
        pass
    except:
        raise f"Fichier {file} introuvable !"
        return

    New_Message = ""
    for Letter in rd:
        if Letter in Keys:
            index = Keys.index(Letter)
            New_Message = str(New_Message) + "." + str(index)
    New_Message = New_Message.replace(",", "")
    return New_Message


def decrypte_with_file(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            rd = f.read()
        pass
    except:
        raise f"Fichier {file} introuvable !"
        return

    New_Message = ""
    m = rd.split(".")
    for Number in m:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            pass
    New_Message = New_Message.replace(",", "")
    return New_Message


def crypte(msg):
    New_Message = ""
    for Letter in msg:
        if Letter in Keys:
            index = Keys.index(Letter)
            New_Message = str(New_Message) + "." + str(index)
    New_Message = New_Message.replace(",", "")
    return New_Message