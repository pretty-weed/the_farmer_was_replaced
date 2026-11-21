

from __builtins__ import Any, string


def zip(a: list | tuple | set, b: list | tuple | set) -> list:
    res = []
    a = list(a)
    b = list(b)
    for i in range(min([len(a), len(b)])):
        res.append((a[i], b[i]))
    return res
def index(container: list | tuple, val: Any) -> int | None:
    for i in range(len(container)):
        if container[i] == val:
            return i
    return None

def split(in_str, splitter):
    res = []
    current = ""
    skip = 0

    if len(in_str) < len(splitter):
        return [in_str]
    i = 0
    for i in range(len(in_str) - len(splitter) + 1):
        if skip:
            skip -= 1
            continue
        hunk = in_str[i:i+len(splitter)]
        if hunk == splitter:
            res.append(current)
            current = ""
            if i == len(in_str) - len(splitter):
                res.append('')
                return res
            skip = len(splitter) -1
        elif len(hunk) < len(splitter):
            res.append(current + hunk)
            break
        else:
            current += in_str[i]
    res.append(current+ in_str[i+1:])
    return res



def get(in_dict, key, default_val=None):
    if key in in_dict:
        return in_dict[key]
    return default_val

def setdefault(in_dict, key, default_val):
    if key in in_dict:
        return in_dict[key]
    in_dict[key] = default_val
    return default_val

def items(in_dict: dict) -> list[tuple[Any, Any]]:
    res = []
    for k in in_dict:
        res.append((k, in_dict[k]))
    return res

def values(in_dict: dict) -> list[Any]:
    res = []
    for k in in_dict:
        res.append(in_dict[k])
    return res

def _multi_split_hunk_helper(in_str:string, cursor: int, splitter_lens) -> list[tuple[int, string]]:
    res = []
    for sl in splitter_lens:
        res.append((sl, in_str[cursor:cursor+sl]))
    return res

def multi_split(in_str, splitters) -> list[string]:
    splitter_lens = {}
    for splitter in splitters:
        setdefault(splitter_lens, len(splitter), []).append(splitter)
    min_split_len = min(splitter_lens)
    max_split_len = max(splitter_lens)
    current = ""
    res = []
    continue_on = True
    skip = 0
    if len(in_str) < min_split_len:
        return [in_str]
    i = 0
    for i in range(len(in_str) - min_split_len + 1):
        if skip:
            skip -= 1
            continue
        
        for split_len, hunk in _multi_split_hunk_helper(in_str, i, splitter_lens):
            if hunk in splitter_lens[split_len]:
                res.append(current)
                current = ""
                skip = split_len -1
                if i == len(in_str) - min_split_len:
                    res.append("")
                    return res
            elif len(hunk) < min_split_len:
                res.append(in_str[i] + current + hunk)
                continue_on = False
                break
            else:
                current += in_str[i]
        if continue_on:
            continue

        
        break
    res.append(current+ in_str[i+1:])
    return res

def format(template, v0=None, v1=None, v2=None, v3=None, v4=None, v5=None, v6=None):
    split_template = multi_split(template, ["%d", "%s"])
    defined = []
    res = ""
    for val in [v0, v1, v2, v3, v4, v5, v5]:
        if val == None:
            break
        defined.append(val)
    
    if len(split_template) -1 != len(defined):
        print("wrong number of values (" + str(len(defined)) + ") [" + str (defined) + "] for template (needs " + str(len(split_template)-1) + ") ["+ template + "]")
        3/0
    for i in range(len(split_template)-1):
        res += split_template[i] + str(defined[i])
    res += split_template[-1]
    return res

def sum(vals: list[int | float] | tuple[int | float] | set[int | float]) -> int | float:
    res = 0
    for val in vals:
        res += val
    return res