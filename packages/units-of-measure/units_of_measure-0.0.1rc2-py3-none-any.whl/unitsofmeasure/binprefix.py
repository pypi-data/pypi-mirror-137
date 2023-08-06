"""Binary Prefixes"""
from unitsofmeasure import Prefix

Ki = Prefix(2, 10, "Ki", "kibi")
Mi = Prefix(2, 20, "Mi", "mebi")
Gi = Prefix(2, 30, "Gi", "gibi")
Ti = Prefix(2, 40, "Ti", "tebi")
Pi = Prefix(2, 50, "Pi", "pebi")
Ei = Prefix(2, 60, "Ei", "exbi")
Zi = Prefix(2, 70, "Zi", "zebi")
Yi = Prefix(2, 80, "Yi", "yobi")

si_binary_prefixes: dict[str, Prefix] = {
    "Ki": Ki,
    "Mi": Mi,
    "Gi": Gi,
    "Ti": Ti,
    "Pi": Pi,
    "Ei": Ei,
    "Zi": Zi,
    "Yi": Yi
}
