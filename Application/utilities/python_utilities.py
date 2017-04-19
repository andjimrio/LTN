from dateutil.parser import parse
from django.utils import timezone


# Busca un valor en un diccionario o un valor dentro de otro.
#       Si no lo encuentra, devuelve una cadena vacía.
def redo_string(dic, string1, string2=None):
    if string2:
        if string1 in dic and string2 in dic[string1]:
            return dic[string1][string2]
        else:
            return ""
    else:
        if string1 in dic:
            return dic[string1]
        else:
            return ""


# Busca un valor de tipo date dentro de un diccionario y lo parsea.
#       Si da error, devuelve una cadena vacía.
def redo_date(dic, string):
    if string in dic:
        try:
            return parse(dic[string])
        except:
            pass

    return timezone.now()