from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict

def sigfigstr(n,sigfigs=4):
    n = float(n)
    sigfigsleft = floor(log10(n)) + 1
    if sigfigsleft > sigfigs:
        n = int(round(n,sigfigs-sigfigsleft))
        return f'{n:0,}'
    else:
        format_str = '{:.' + str(sigfigs-sigfigsleft) + 'f}'
        return format_str.format(n)
    
def boltText(bolt, n, dmin, dbsc, d1bsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs, UTSn, LE):

    text = ''

    # Check output
    if bolt != 'customSelection':
        if n <= 0:
            return 'Threads per inch must be greater than zero'
        if dmin <= 0:
            return 'x must be greater than zero'
        if dbsc <= 0:
            return 'x must be greater than zero'
        if d1bsc <= 0:
            return 'x must be greater than zero'
        if d2min <= 0:
            return 'x must be greater than zero'
        if d2bsc <= 0:
            return 'x must be greater than zero'
        if D1bsc <= 0:
            return 'x must be greater than zero'
        if D1max <= 0:
            return 'x must be greater than zero'
        if D2max <= 0:
            return 'x must be greater than zero'
        if UTSs <= 0:
            return 'x must be greater than zero'
        if UTSn <= 0:
            return 'x must be greater than zero'
        if LE <= 0:
            return 'x must be greater than zero'
    
    else:
        n = ASME_B11_UN_2A2B_dict[bolt]['n']
        dmin = ASME_B11_UN_2A2B_dict[bolt]['dmin']
        dbsc = ASME_B11_UN_2A2B_dict[bolt]['dbsc']
        d1bsc = ASME_B11_UN_2A2B_dict[bolt]['d1bsc']
        d2min = ASME_B11_UN_2A2B_dict[bolt]['d2min']
        d2bsc = ASME_B11_UN_2A2B_dict[bolt]['d2bsc']
        D1bsc = ASME_B11_UN_2A2B_dict[bolt]['D1bsc']
        D1max = ASME_B11_UN_2A2B_dict[bolt]['D1max']
        D2max = ASME_B11_UN_2A2B_dict[bolt]['D2max']
        UTSs = ASME_B11_UN_2A2B_dict[bolt]['UTSs']
        UTSn = ASME_B11_UN_2A2B_dict[bolt]['UTSn']
        LE = ASME_B11_UN_2A2B_dict[bolt]['LE']

    text += f'''
    <p>Hello</p> 
    <p>{{{'%.2f'%n}}}</p>   
    '''

    return text
