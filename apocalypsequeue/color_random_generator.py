import random


out1 = []

for i in range(0,20):
    r = random.randint(50,256)
    g = random.randint(50,256)
    b = random.randint(50,256)
    rgb = u'#{:x}{:x}{:x}'.format(r, g, b)
    out = u'''    "#ShelfButton_{0}":
    {{
        "colours":
        {{
            "normal_border": "{1}",
            "hovered_border": "{1}",
            "selected_border": "{1}"
        }}
    }},'''.format(i, rgb)
    out1.append(u"SHELF_{0} = ({1}, {2}, {3}) {4}".format(i, r,g,b,rgb))
    print(out)


for o in out1:
    print(o)