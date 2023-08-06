import re
import math

MAG_DICT = {'K': 3, 'M': 6, 'B': 9, 'T': 12, 'q': 15, 'Q': 18, 's': 21, 'S': 24, 'o': 27, 'N': 30, 'd': 33, 'U': 36, 'D': 39, 'Td': 42, 'qd': 45, 'Qd': 48, 'sd': 51, 'Sd': 54, 'Od': 57, 'Nd': 60, 'V': 63, 'uV': 66, 'dV': 69, 'tV': 72, 'qV': 75, 'QV': 78, 'sV': 81, 'SV': 84, 'OV': 87, 'NV': 90, 'tT': 93}

mag_rex = '|'.join(list(MAG_DICT.keys()))
regex_search= f"(\d*\.?\d*)?({mag_rex})\\Z"

def mag_out(num,kk,cc=3):
    # kk - digits before dot , cc - digits after dot
    fmt = '{0:.'+str(kk+cc-1)+'e}'
    ss = fmt.format(num)
    s1 = ss.replace('.','')
    p1 = s1.split('e')
    a1 = p1[0]
    a2 = int(p1[1])
    return '{0}.{1}e{2}'.format(a1[0:kk],a1[kk:],a2-kk+1)

def mag_to_int(x):
    match = re.search(regex_search,x)
    if match is not None:
        quantity = float(match.group(1))
        magnitude = 10 ** MAG_DICT[match.group(2)]
        return (quantity * magnitude)
    else:
        try:
            return int(x)
        except ValueError as exc:
            raise ValueError('Not a valid Magnitude') from exc

def int_to_mag(x):
    mag_val = int(math.log10(x))
    dp =  (mag_val % 3) +1
    mag_val = mag_val - (mag_val % 3)
    mag_abb = list(MAG_DICT.keys())[list(MAG_DICT.values()).index(mag_val)]
    out = mag_out(x,dp)[:4+dp] + mag_abb



    return out



