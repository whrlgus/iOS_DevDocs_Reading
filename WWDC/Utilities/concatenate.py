from collections import OrderedDict

input_vtt = '225.vtt'
output_vtt = '255con.vtt'

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
    if len(b) == 1:
        new += (ele + "\n\n")
        continue

    chunk = b[1].strip()
    if chunk[-1] in ['.', '?']:
        if time == "":
            new += (ele + "\n\n")
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
