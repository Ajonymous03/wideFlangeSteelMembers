from flask import request
from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict
from dictionaries.boltEquations import *

def sigfigstr(n,sigfigs=4):
    n = float(n)
    sigfigsleft = floor(log10(n)) + 1
    if sigfigsleft > sigfigs:
        n = int(round(n,sigfigs-sigfigsleft))
        return f'{n:0,}'
    else:
        format_str = '{:.' + str(sigfigs-sigfigsleft) + 'f}'
        return format_str.format(n)
    
def boltText(bolt, n, dmin, dbsc, d2min, D1bsc, D1max, D2max, UTSs, UTSn, LE):
    # Gets bolt data

    text = f'''<form action="/bolt" method="POST">
    <div class="section">
        <div class="header col-4">
        <h1>Bolt Calculator</h1>
        </div>
    </div>
    <div class="section">
        <div class="col-3">
        <label
            class="bolt_select_label"
            for="boltDropdown"
            style="vertical-align: middle"
            >Selected Bolt:
        </label>
        <select class="boltDropdown" id="boltDropdown" name="boltDropdown">
            <option id="1/4-20" value="1/4-20">1/4-20</option>
            <option id="1/4-28" value="1/4-28">1/4-28</option>
            <option id="1/2-13" value="1/2-13">1/2-13</option>
            <option id="1/2-20" value="1/2-20">1/2-20</option>
            <option id="3/4-10" value="3/4-10">3/4-10</option>
            <option id="3/4-16" value="3/4-16">3/4-16</option>
            <option id="1-8" value="1-8">1-8</option>
            <option id="1-14" value="1-14">1-14</option>
        </select>
        </div>
        <script>
        document.getElementById("boltDropdown").onchange = function () {{
            sessionStorage.setItem(
            "boltSelectItem",
            document.getElementById("boltDropdown").value
            );
            this.form.submit();
        }};

        if (sessionStorage.getItem("boltSelectItem")) {{
            document.getElementById("boltDropdown").options[
            sessionStorage.getItem("boltSelectItem")
            ].selected = true;
        }}
        </script>
        <div class="col-3">
        <label class="boltInputLabel" for="UTSs"
            >UTSs (Strength of Externally Threaded Part) :
        </label>
        <input
            class="boltInput"
            type="text"
            id="UTSs"
            value="{'%g'%(UTSs)}"
            name="UTSs"
        />
        <label class="unit">???</label>

        <label class="boltInputLabel" for="UTSn"
            >UTSn (Strength of Internally Threaded Part) :
        </label>
        <input
            class="boltInput"
            type="text"
            id="UTSn"
            value="{'%g'%(UTSn)}"
            name="UTSn"
        />
        <label class="unit">???</label>

        <label class="boltInputLabel" for="LE"
            >LE (Length of Engagement) :
        </label>
        <input
            class="boltInput"
            type="text"
            id="LE"
            value="{'%g'%(LE)}"
            name="LE"
        />
        <label class="unit">???</label>
        </div>
    </div>
    <hr />'''
    
    
    if bolt == None:
        return text
    else:
        pVar = sigfigstr(p(n))
        HVar = sigfigstr(H(n))
        d1bscVar = sigfigstr(D1bsc)
        d2bscVar = sigfigstr(d2bsc(dbsc, H(n)))
        AbscVar = sigfigstr(Absc(dbsc))
        As1a = sigfigstr(As_FEDSTD_1a(d2bsc(dbsc, H(n)), H(n)))
        As1b = sigfigstr(As_FEDSTD_1b(dbsc, n))

        # Based off of Alexander 1977 Text and Wide Flange Page Text
        text += f'''
        <h1>Geometric Properties</h1>
        <h4>From ASME B1.1-2019, the dimensions of a {bolt} fastener are: </h4>
        <p>$n = {n}$ (UNITS)</p>
        <p>$P = \\frac{{1}}{{n}} = \\frac{{1}}{n} = {pVar} $ (UNITS)</p>
        <p>$H = \\frac{{\\sqrt{3}}}{{2n}} = \\frac{{\\sqrt{3}}}{{2({n})}} = {HVar} $ (UNITS)</p>
        <p>$d_{{min}} = {dmin}$ (UNITS)</p>
        <p>$d_{{bsc}} = {dbsc}$ (UNITS)</p>
        <p>$d_{{2,min}} = {d2min}$ (UNITS)</p>
        <p>$D_{{1,bsc}} = d_{{1,bsc}} = {D1bsc}$ (UNITS)</p>
        <p>$D_{{1,max}} = {D1max}$ (UNITS)</p>
        <p>$D_{{2,bsc}} = d_{{2,bsc}} = {d2bscVar}$ (UNITS)</p>
        <p>$D_{{2,max}} = {D2max}$ (UNITS)</p>
        '''


        # How to say "they can be simplified to be exactly the same" in a short, concise manner? Currently I have "geometrically identical"
        text += f'''
        <h1>Tensile Stress Area</h1>
        <h4>The ultimate tensile strength of a threaded fastener is directly proportional to the actual cross sectional area.</h4>
        <h4>ASME B1.1-2019 provides two equations to calculate the tensile stress area, both of which are geometrically identical: </h4>
        <p>$A_{{s, 1a}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}}$</p>
        <p>$= \\pi\\left(\\frac{{{d2bscVar}}}{{2}}-\\frac{{3({HVar})}}{{16}}\\right)^{{2}}$</p>
        <p>$= {{{As1a}}}$ (UNITS)</p>
        </br>
        <p>$A_{{s, 1b}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{9\\sqrt{{3}}}}{{16n}}\\right)^{{2}}$</p>
        <p>$= \\frac{{\\pi}}{{4}}\\left({dbsc} - \\frac{{9\\sqrt{{3}}}}{{16({n})}}\\right)^{{2}}$</p>
        <p>$= {{{As1b}}}$ (UNITS)</p>
        '''

        return text
