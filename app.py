from PIL import Image  # type:ignore
import os
import numpy
from noise import snoise2  # type:ignore
import random
from opensimplex import OpenSimplex  # type:ignore # lacking in methods

A4 = 794, 1123

dir = os.listdir("./data/")
d = {}

for i in dir:
    d[i[0]] = [Image.open(f"./data/{i}/{im}") for im in os.listdir(f"./data/{i}/")]

im = Image.new("RGBA", A4, (0xFF, 0xFF, 0xFF, 0xFF))
nm = numpy.array(im)


def white_nose(w, h, f, o):
    a = int(abs(0x7F * snoise2(w / f, h / f, o))) + 0x7F
    if a < 0xC8:
        a = random.choice([0xD0, 0xD2, 0xD4])
    return a


octaves = random.randint(16, 32)
freq = (fr := float(random.randint(1, 16))) * octaves
for h in range(A4[1]):
    for w in range(A4[0]):
        nm[h, w] = (a := (white_nose(w, h, freq, octaves)), a, a, 0xFF)

im = Image.fromarray(nm)
print(f"f: {fr}, oct = {octaves}")


def pm(y):
    return y + random.choice([0, 0, 0, 3, 2, 1])


def typechars(typethis):
    typethis = typethis.split("\n")
    typethese = []
    for i in typethis:
        typethese.append(i.split(" "))

    x = random.randint(20, 50)
    y = random.randint(32, 40)
    slant = 0

    for i in typethese:
        for j in i:
            if len(j) * 18 + x > A4[0]:
                r = random.choice([32, 36, 40])
                y += r
                y - random.randint(slant // 2, slant)
                x = random.randint(20, 50)
                slant = 0
                if y > A4[1] - 50:
                    return j
            for k in j:
                if k in ("f", "g", "j", "p", "q", "y", "G"):
                    im.paste(
                        a := random.choice(d[k]), (x, (slant := pm(slant)) + y + 8), a
                    )
                elif k == "‘" or k == "’":
                    im.paste(
                        a := random.choice(d["'"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == ".":
                    im.paste(
                        a := random.choice(d["☺"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == ">":
                    im.paste(
                        a := random.choice(d["♥"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == "<":
                    im.paste(
                        a := random.choice(d["♦"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == "*":
                    im.paste(
                        a := random.choice(d["♠"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == ":":
                    im.paste(
                        a := random.choice(d["○"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == "/":
                    im.paste(
                        a := random.choice(d["•"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == "|":
                    im.paste(
                        a := random.choice(d["◘"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == "-":
                    im.paste(
                        a := random.choice(d["♣"]), (x, (slant := pm(slant)) + y), a
                    )
                elif k == '"':
                    im.paste(
                        a := random.choice(d["☻"]), (x, (slant := pm(slant)) + y - 8), a
                    )
                else:
                    im.paste(a := random.choice(d[k]), (x, (slant := pm(slant)) + y), a)
                x += random.randint(15, 16)
            r = random.randint(16, 30)
            x += r
        r = random.choice([32, 36, 40])
        y += r
        y - random.randint(slant // 2, slant)
        if y > A4[1] - 50:
            return i
        x = random.randint(20, 50)
        slant = 0

    # for i in typethis:
    #     if i == '\n':
    #         r = random.choice([28, 32, 36])
    #         y += r
    #         x = 20-16
    #     elif i == ' ':
    #         r = random.choice([16, 8, 4, 2])
    #         x += r
    #     elif i in ('f', 'g', 'j', 'p', 'q', 'y'):
    #         if x > 794-48:
    #             im.paste(a := random.choice(d['—']), (pm(x), y+8), a)
    #             y += 30
    #             x = random.randint(18, 22)
    #         im.paste(a := random.choice(d[i]), (pm(x), y+8), a)
    #     else:
    #         if x > 794-48:
    #             im.paste(a := random.choice(d['—']), (pm(x), y), a)
    #             y += 30
    #             x = random.randint(18, 22)
    #         im.paste(a := random.choice(d[i]), (pm(x), y), a)
    #     x += 16
    #     if x > 794-24:
    #         y += 30
    #         x = random.randint(18, 22)
    # return x, y


t = typechars(
    """
— management pressure - Is there pressure to achieve. Is the interaction carried out in the presence of management
— motivation - What motivates the interaction, Does this encourage or discourage experimentation
— organizational goals - What is the objective of the organization. (profit, education, etc.) How does this affect the interaction
— organizational decision making - Who determines the systems that you use

4. The concept of Interaction Styles refers to all the ways the user can communicate or otherwise interact with the computer system. The concept belongs in the realm of HCI or at least have its roots in the computer medium, usually in the form of a workstation or a desktop computer. These concepts do however retain some of their descriptive powers outside the computer medium. These 4 are:
a. Command language (or command entry)
b. Form filling
c. Menu selection
d. Direct manipulation

"""
)
print(t)

im.show()
im.save("./1.png")
