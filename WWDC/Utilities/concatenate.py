import sys
from collections import OrderedDict

input_vtt = sys.argv[1]
inputNameElements = sys.argv[1].split(".")
output_vtt = inputNameElements[0] + "con." + inputNameElements[1]

f = open(input_vtt, "r")
string = f.read()
f.close()
a = list(OrderedDict.fromkeys(string.split("\n\n")))

new = ""
time = ""
tmp = ""
for ele in a:
    b = ele.split("\n")
    c = b[0].split(" --> ")
    if len(b) == 1 or b[0] == "" or ele.startswith("WEBVTT"):
        new += (ele + "\n\n")
        continue
        
    chunk = " ".join( x.strip() for x in b[1:] ).strip()
    if chunk[-1] in ['.', '?']:
        if time == "":
            new += (b[0] + "\n" + chunk + "\n\n")
        else:
            time += " --> " + c[1]
            tmp += chunk
            new += (time + "\n" + tmp + "\n\n")
            time = ""
            tmp = ""
    elif time == "":
        time = c[0]
        tmp += (chunk + " ")
    else:
        tmp += (chunk + " ")



f = open(output_vtt, "w")
f.write(new)
f.close()
