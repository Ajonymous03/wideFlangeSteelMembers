from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict
from dictionaries.threads import *
from .string_functions import htmlstr, sigfigstr


def boltText_header():
    text = htmlstr(default_indent=10);
    text.newline('Bolt Tensile Strength Calculation According to FED-STD-H28/2B', tag='h1')
    return text.string


def boltText_input(UTSs_str,UTSn_str,LE_str):
    text = htmlstr(default_indent=10);
    text.newline(r'<div class="col-3">')
    text.newline(r'  <div style = "text-align: center";>')
    text.newline(r'    <label class="bolt_select_label" for="boltDropdown" style="vertical-align: middle" >Selected Bolt:</label>')
    text.newline(r'    <select class="boltDropdown" id="boltDropdown" name="boltDropdown">')
    text.newline(r'      <option id="1/4-20" value="1/4-20">1/4-20</option>')
    text.newline(r'      <option id="1/4-28" value="1/4-28">1/4-28</option>')
    text.newline(r'      <option id="1/2-13" value="1/2-13">1/2-13</option>')
    text.newline(r'      <option id="1/2-20" value="1/2-20">1/2-20</option>')
    text.newline(r'      <option id="3/4-10" value="3/4-10">3/4-10</option>')
    text.newline(r'      <option id="3/4-16" value="3/4-16">3/4-16</option>')
    text.newline(r'      <option id="1-8" value="1-8">1-8</option>')
    text.newline(r'      <option id="1-14" value="1-14">1-14</option>')
    text.newline(r'    </select>')
    text.newline(r'  </div>')
    text.newline(r'  <button class = "button1" style = "display: flex; flex-wrap: wrap;" type = "submit">Calculate</button>')
    text.newline(r'</div>')
    text.newline(r'<script>')
    text.newline(r'  document.getElementById("boltDropdown").onchange = function () {')
    text.newline(r'    sessionStorage.setItem("boltSelectItem",document.getElementById("boltDropdown").value);')
    text.newline(r'    this.form.submit();')
    text.newline(r'  };')
    text.newline(r'')
    text.newline(r'  if (sessionStorage.getItem("boltSelectItem")) {')
    text.newline(r'    document.getElementById("boltDropdown").options[sessionStorage.getItem("boltSelectItem")].selected = true;')
    text.newline(r'  }')
    text.newline(r'</script>')
    text.newline(r'<div class="col-3">')
    text.newline(r'  <label class="boltInputLabel" for="UTSs"')
    text.newline(r'    >UTSs (Strength of Externally Threaded Part) :')
    text.newline(r'  </label>')
    text.newline(r'  <input class="boltInput" type="text" id="UTSs" value=' + f'"{UTSs_str}"' + r' name="UTSs"/>')
    text.newline(r'  <label class="unit">psi</label>')
    text.newline(r'')
    text.newline(r'  <label class="boltInputLabel" for="UTSn">UTSn (Strength of Internally Threaded Part) :</label>')
    text.newline(r'  <input class="boltInput" type="text" id="UTSn" value=' + f'"{UTSn_str}"' + r' name="UTSn"/>')
    text.newline(r'  <label class="unit">psi</label>')
    text.newline(r'')
    text.newline(r'  <label class="boltInputLabel" for="LE">LE (Length of Engagement) :</label>')
    text.newline(r'  <input class="boltInput" type="text" id="LE" value='+ f'"{LE_str}"' + r'name="LE" />')
    text.newline(r'  <label class="unit">in.</label>')
    text.newline(r'</div>')
    return text.string
    
def boltText_output(bolt, UTSs_str,UTSn_str,LE_str):
    text = htmlstr(default_indent=10);
    
    text.newline('<h1>Input Echo</h1>')
    text.newline('<p>' + f'Bolt: {bolt}' + r'</p>')
    text.newline('<p>' + f'UTSs: {UTSs_str} psi' + r'</p>')
    text.newline('<p>' + f'UTSn: {UTSn_str} psi' + r'</p>')
    text.newline('<p>' + f'LE: {LE_str} in.' + r'</p>')    
    
    # Check input and convert to numbers
    bad_input = False
    try:
        UTSs = float(UTSs_str)
    except:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the externally threaded part must be a number</p>')

    try:
        UTSn = float(UTSn_str)
    except:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the internally threaded part must be a number</p>')

    try:
        LE = float(LE_str)
    except:
        bad_input = True
        text.newline(r'<p>The length of engagement must be a number</p>')        
    
    if bad_input:
        return text.string
        
    if UTSs <= 0:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the externally threaded part must be a positive number</p>')

    if UTSn <= 0:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the internally threaded part must be a positive number</p>')
        
    if LE <= 0:
        bad_input = True
        text.newline(r'<p>The length of engagement must be a positive number</p>')
    
    if bad_input:
        return text.string    
    
    # Thread Form Dimensions
    thread_data = ASME_B11_UN_2A2B_dict[bolt]
    boltObj = Assembly(thread_data, UTSs, UTSn)

    text.newline('Thread Form Dimensions', tag='h1')
    text.newline(f'A {bolt} thread has a nominal size of ' + sigfigstr(boltObj.dbsc) + ' in. and ' + str(boltObj.n) + ' threads/in.', tag='p')
    text.newline(r'$d = ' + sigfigstr(boltObj.dbsc) + r'\text{ in.}$',tag='p')
    text.newline(r'$n = ' + str(boltObj.n) + r'\text{ threads/in.}$',tag='p')
    
    text.newline(f'Based on the basic profile for UN screw threads shown in ASTM B1.1-2019 Figure 2, basic thread dimensions are:', tag='p')    
    text.newline(r'$p = \dfrac{1}{n} = \dfrac{1}{' + str(boltObj.n) + r'\text{ threads/in.}} = ' + sigfigstr(1/boltObj.n) + r'\text{ in.}$',tag='p')
    text.newline(r'$H = \dfrac{\sqrt{3}}{2n} = \dfrac{\sqrt{3}}{2(' + str(boltObj.n) + r'\text{ threads/in.})} = ' + sigfigstr(sqrt(3)/2/boltObj.n) + r'\text{ in.}$',tag='p')
    
    text.newline(r'$D_{1,bsc} = d_{1,bsc} = ' + sigfigstr(boltObj.D1bsc) + r'$ in.', tag='p')
    text.newline(r'$D_{2,bsc} = d_{2,bsc} = ' + sigfigstr(boltObj.D2bsc) + r'$ in.', tag='p')

    text.newline(f'From ASME B1.1-2019 Table 2A, the minimum dimensions of the external threads are:', tag='p')
    text.newline(r'$d_{min} = ' + sigfigstr(boltObj.dmin) + r'\text{ in.}$',tag='p')
    text.newline(r'$d_{2,min} = ' + sigfigstr(boltObj.d2min) + r'\text{ in.}$',tag='p')
    
    text.newline(f'From ASME B1.1-2019 Table 2B, the maximum dimensions of the internal threads are:', tag='p')
    text.newline(r'$D_{1,max} = ' + sigfigstr(boltObj.D1max) + r'\text{ in.}$',tag='p')
    text.newline(r'$D_{2,max} = ' + sigfigstr(boltObj.D2max) + r'\text{ in.}$',tag='p')
    
    
    text.newline(f'Tensile Strength', tag='h1')
    text.newline(f'The ultimate tensile strength of a threaded fastener is directly proportional to the cross sectional area through the threaded region.', tag='p')
    text.newline(f'FED-STD-H28/2B provides two equations to calculate the tensile stress area, both of which are geometrically identical',tag='p')
    # text.newline(r'$A_{s,1a} = \pi\left(\dfrac{d_{2,bsc}}{2} - \dfrac{3H}{16}\right)^{2} = \pi\left(\left(\dfrac{1}{2}\right)\left(d_{2,bsc} - \dfrac{3H}{8}\right)\right)^{2} = \dfrac{\pi}{4}\left(d_{2,bsc} - \dfrac{3H}{8}\right)^{2}$', tag='p')
    # text.newline(r'$A_{s,1b} = \dfrac{\pi}{4}\left(d_{bsc} - \dfrac{0.9743}{n}\right)^{2} = \dfrac{\\pi}{4}\left(d_{bsc} - \dfrac{9P\sqrt{3}}{16}\right)^{2} = \dfrac{\pi}{4}\left(d_{bsc} - \dfrac{9\sqrt{3}\left(\dfrac{2H}{\sqrt{3}}\right)}{16}\right)^{2} = \dfrac{\pi}{4}\left(d_{bsc} - \dfrac{9H}{8}\right)^{2}$', tag='p')
    # text.newline(f'Figure 2 in ASME B1.1-2019 provides thread geometry to further prove the equality:', tag='p')
    # text.newline(r'$d_{2,bsc} = d_{bsc} - 2\left(\dfrac{3H}{8}\right) = d_{bsc} - \dfrac{6H}{8}', tag='p')    
    # text.newline(r'$A_{s, 1a} = \frac{\pi}{4}\left(d_{bsc} - \dfrac{6H}{8} - \dfrac{3H}{8}\right)^{2} = \dfrac{\pi}{4}\left(d_{bsc} - \dfrac{9H}{8}\right)^{2} = A_{s, 1b}$', tag='p')  
    text.newline(r'For this example, equation $A_{s, 1a}$ will be used', tag='p')
    text.newline(r'$A_{s, 1a} = \pi\left(\dfrac{d_{2,bsc}}{2}-\dfrac{3H}{16}\right)^{2}$', tag='p')   
    text.newline(r'$= \pi\left(\dfrac{' + sigfigstr(boltObj.d2bsc) + r'}{2} - \dfrac{3(' + sigfigstr(boltObj.H) + r')}{16}\right)^{2}$', tag='p') 
    text.newline(r'$= ' + sigfigstr(boltObj.As_FEDSTD_1a()) + r' \text{ in.}^{2}$', tag='p')
    text.newline(f'The tensile strength of a threaded fastener is equal to:', tag='p')
    text.newline(r'$P = \dfrac{F}{A} \therefore F = PA$', tag='p')    
    text.newline(r'$F = UTSs\left(A_{s,1a}\right) = ' + str(boltObj.UTSs) + r'\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\right) = ' + sigfigstr(boltObj.UTSs * boltObj.As_FEDSTD_1a()) + r'\text{ lbs}$', tag='p')  
    text.newline(f'Length of Engagement', tag='h1')
    text.newline(f'The length of engagement is the measured length of interaction between a fastener and its mating material', tag='p')
    text.newline(f'The method of failure for a fastener is dependent on the length of engagement', tag='p')
    text.newline(f'FED-STD-H28/2B provides equations to calculate the length of engagement to ensure a specific mode of failure', tag='p')
    text.newline(r'$R_{1} = \dfrac{AS_{s,max}}{AS_{n,min}}$', tag='p')
    text.newline(r'$= \dfrac{\pi\dfrac{3}{4}D_{1,bsc}LE}{\pi d_{min}\left(\dfrac{1}{2n} + \dfrac{1}{\sqrt{3}}\left(d_{min} - D_{2,max}\right)\right)LE}$', tag='p')   
    text.newline(r'$= \dfrac{\pi\dfrac{3}{4}\left(' + sigfigstr(boltObj.D1bsc) + r'\right)}{\pi\left(' + str(boltObj.dmin) + r'\right)\dfrac{1}{2\left(' + str(boltObj.n) + r'\right)} + \dfrac{1}{\sqrt{3}}\left(\left(' + str(boltObj.dmin) + r'\right) - \left(' + str(boltObj.D2max) + r'\right)\right)}$', tag='p')   
    text.newline(r'$ = ' + sigfigstr(boltObj.ASs_max_FEDSTD_6b() / boltObj.ASn_min_FEDSTD_2a()) + r'$', tag='p')
    text.newline(r'$R_{2} = \dfrac{UTSn}{UTSs} = ' + sigfigstr(boltObj.UTSn / boltObj.UTSs) + '$', tag='p')   
    text.newline(r'$\dfrac{R_{1}}{R_{2}} = ' + sigfigstr((boltObj.ASn_min_FEDSTD_2a() / boltObj.ASs_max_FEDSTD_6b()) / (boltObj.UTSn / boltObj.UTSs)) + r'$', tag='p')  
    
    if (boltObj.ASn_min_FEDSTD_2a() / boltObj.ASs_max_FEDSTD_6b()) / (boltObj.UTSn / boltObj.UTSs) < 1:
        text.newline(r'$Because \dfrac{R_{1}}{R_{2}}$ < 1, external thread failure controls and FED-STD-H28/2B Formula (15) is used', tag='p')  
        text.newline(r'$A_{s} = \pi\left(\dfrac{d_{2,bsc}}{2} - \dfrac{3H}{16}\right)^{2} = $', tag='p')   
        text.newline(r'$\pi\left(\dfrac{' + sigfigstr(boltObj.d2bsc) + r'}{2} - \dfrac{3\left(' + sigfigstr(boltObj.H) + r'\right)}{16}\right)^{2} = ' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}$', tag='p')
        text.newline(r'$AS_{s,min} = \pi d_{min}\left(\dfrac{1}{2n} + \dfrac{1}{\sqrt{3}}\left(d_{min} - D_{2,max}\right)\right)LE = \pi\left(' + str(boltObj.dmin) + r'\right)\left(\dfrac{1}{2\left(' + 
                     str(boltObj.n) + r'\right)} + \dfrac{1}{\sqrt{3}}\left(' + str(boltObj.dmin) + r' - ' + str(boltObj.D2max) + r'\right)\right)\left(' + str(LE) + r'\right) = ' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}^{2}$', tag='p')
        text.newline(r'$LE = \dfrac{2A_{s}}{AS_{s,min}} = \dfrac{2\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\right)}{' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'} = ' + sigfigstr(2 * boltObj.As_FEDSTD_1a() / boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}$', tag='p')
    else:
        text.newline(r'Because $\dfrac{R_{1}}{R_{2}}$ > 1, either internal thread failure or combined failure controls and FED-STD-H28/2B Formula (13) or (16) is used', tag='p')
        text.newline(r'$A_{s} = \pi\left(\frac{d_{2,bsc}}{2}-\frac{3H}{16}\right)^{2}$', tag='p')
        text.newline(r'$= \pi\left(\frac{' + sigfigstr(boltObj.d2bsc) + r'}{2} - \frac{3\left(' + sigfigstr(boltObj.H) + r'\right)}{16}\right)^{2} =' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in}^{2}$', tag='p')
        text.newline(r'$AS_{s,min} = \pi d_{min}\left(\dfrac{1}{2n} + \dfrac{1}{\sqrt{3}}\left(d_{min} - D_{2,max}\right)\right)LE = \pi\left(' + str(boltObj.dmin) + r'\right)\left(\dfrac{1}{2\left(' + 
                     str(boltObj.n) + r'\right)} + \dfrac{1}{\sqrt{3}}\left(' + str(boltObj.dmin) + r' - ' + str(boltObj.D2max) + r'\right)\right)\left(' + str(LE) + r'\right) = ' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}^{2}$', tag='p')
        text.newline(r'$LE_{r,13} = \dfrac{4A_{s}}{\pi d_{2,bsc}} = \dfrac{4\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\right)}{\pi\left(' + str(boltObj.d2bsc) + r'\right)} = ' + sigfigstr(boltObj.LEr_FEDSTD_13()) + r'\text{ in.}$', tag='p')
        text.newline(r'$LE_{r,16} = \dfrac{\dfrac{2A_{s}}{AS_{n}}}{R_{2}} = \dfrac{\dfrac{2\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\right)}{' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'}}{' + sigfigstr(boltObj.UTSn / boltObj.UTSs) + r'} = ' + sigfigstr(boltObj.LEr_FEDSTD_16()) + r'\text{ in.}$', tag='p')
        text.newline(r'The controlling length of engagement is the maximum of $LE_{r,13}$ and $LE_{r,16}$', tag='p')
        
        if boltObj.LEr_FEDSTD_13() > boltObj.LEr_FEDSTD_16():
            text.newline(r'Thus, $LE = LE_{r,13} = ' + sigfigstr(boltObj.LEr_FEDSTD_13()) + r'\text{ in.}$', tag='p')
        else:
            text.newline(r'Thus, $LE = LE_{r,16} = ' + sigfigstr(boltObj.LEr_FEDSTD_16()) + r'\text{ in.}$', tag='p')
    return text.string

def boltText_footer():
    text = htmlstr(default_indent=10);
    text.newline('Developed by Jonathan Smith and Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
    text.newline('This work was supported by the Naval Engineering Education Consortium [Award Number N00174-22-1-0017].', tag='p')
    return text.string
