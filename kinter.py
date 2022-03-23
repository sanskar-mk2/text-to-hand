import tkinter as tk
import logging
from noise import snoise2  # type:ignore
import random
import numpy  # type:ignore
from palette import Palette
from PIL import Image, ImageTk  # type:ignore
import os
from pypresence import Presence  # type:ignore
import time

client_id = "851555374020558859"
A4 = 794, 1123
A4X = tuple([int(i // 1.5) for i in A4])
print(A4X)

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
pal = Palette(temptress="#29161d", wewak="#fa9495")


class Writer:
    im = Image.new("RGBA", A4, (0xFF, 0xFF, 0xFF, 0xFF))
    nm = numpy.array(im)
    octaves = 0
    freq = 0
    rpcimagestate = 36
    RPC = Presence(client_id)
    RPC.connect()
    samay = time.time() - 10000.0
    lines: list = list()

    def __init__(self, tkinter_instance=None):
        self.thekinter = tkinter_instance
        # self.logo_img = ImageTk.PhotoImage(Image.open("lain.png").resize((64, 64)))
        # self.logo_image_label.grid(row=0, column=0)
        self.tinker_sheet = ImageTk.PhotoImage(self.im.resize(A4X))
        self.tinker_sheet_label = tk.Label(self.thekinter, image=self.tinker_sheet)
        self.tinker_sheet_label.grid(row=0, column=6, rowspan=3)
        self.d = dict()
        for i in os.listdir("./data/"):
            self.d[i[0]] = [
                Image.open(f"./data/{i}/{im}") for im in os.listdir(f"./data/{i}/")
            ]
        self.im_ki_copy = self.im.copy()
        self.rpc_change_icon = tk.Button(
            self.thekinter,
            text=str(self.rpcimagestate),
            bg=pal.colors["temptress"],
            fg=pal.colors["wewak"],
            command=self.updaterpcimage,
        )
        self.rpc_change_icon.grid(row=0, column=5)
        self.rpc_images = dict()
        for i in next(os.walk("./lains/"))[2]:
            self.rpc_images[int(i.split(".")[0])] = ImageTk.PhotoImage(
                Image.open(f"./lains/{i}").resize((64, 64))
            )

        self.line_entry_h = tk.Entry(
            self.thekinter, bg=pal.colors["temptress"], fg=pal.colors["wewak"]
        )
        self.line_entry_h.grid(column=1, row=1)
        self.line_entry_v = tk.Entry(
            self.thekinter,
            bg=pal.colors["temptress"],
            fg=pal.colors["wewak"],
        )
        self.line_entry_v.grid(column=3, row=1)

        self.hlinebutton = tk.Button(
            self.thekinter,
            text="Horizontal Line",
            bg=pal.colors["temptress"],
            fg=pal.colors["wewak"],
            command=lambda: self.addline(vh="h", pos=self.line_entry_h.get()),
        )
        self.hlinebutton.grid(column=2, row=1)
        self.vlinebutton = tk.Button(
            self.thekinter,
            text="Vertical Line",
            bg=pal.colors["temptress"],
            fg=pal.colors["wewak"],
            command=lambda: self.addline(vh="v", pos=self.line_entry_v.get()),
        )
        self.vlinebutton.grid(column=4, row=1)

        self.RPC.update(
            state="Running on NAVI v4.0",
            details="Tachibana Lab",
            large_image=str(self.rpcimagestate),
            small_image="copland",
            large_text="Lain",
            small_text="Copland OS Enterprise",
            start=self.samay,
        )
        self.logo_image_label = tk.Label(image=self.rpc_images[self.rpcimagestate])
        self.logo_image_label.grid(row=0, column=0)

    def drawline(self, xy, vh):
        if vh == "v":
            a = random.choice(self.d["ñ"])
            self.im.paste(
                a,
                xy,
                a,
            )
        elif vh == "h":
            a = random.choice(self.d["ñ"])
            a = a.rotate(90, expand=1)
            a.show()
            self.im.paste(a, xy, a)

    def addline(self, vh, pos):
        if vh == "v":
            pos = int(pos), 0
        elif vh == "h":
            pos = 0, int(pos)
        self.lines.append([pos, vh])

    def updaterpcimage(self):
        self.rpcimagestate += 1
        self.rpcimagestate %= len(self.rpc_images)
        self.RPC.update(
            state="Running on NAVI v4.0",
            details="Tachibana Lab",
            large_image=str(self.rpcimagestate),
            small_image="copland",
            large_text="Lain",
            small_text="Copland OS Enterprise",
            start=self.samay,
        )
        self.logo_image_label.grid_forget()
        self.logo_image_label = tk.Label(image=self.rpc_images[self.rpcimagestate])
        self.logo_image_label.grid(row=0, column=0)
        self.rpc_change_icon.grid_forget()
        self.rpc_change_icon = tk.Button(
            self.thekinter,
            text=str(self.rpcimagestate),
            bg=pal.colors["temptress"],
            fg=pal.colors["wewak"],
            command=self.updaterpcimage,
        )
        self.rpc_change_icon.grid(row=0, column=5)

    def white_noise(self, w, h, f, o):
        a = int(abs(0x7F * snoise2(w / f, h / f, o))) + 0x7F
        if a < 0xD8:
            a = random.choice([0xD0, 0xD2, 0xD4])
        return a

    def create_new_page(self):
        octaves = random.randint(16, 32)
        freq = (float(random.randint(1, 16))) * octaves
        self.freq = freq
        self.octaves = octaves
        for h in range(A4[1]):
            for w in range(A4[0]):
                self.nm[h, w] = (
                    a := (self.white_noise(w, h, freq, octaves)),
                    a,
                    a,
                    0xFF,
                )
        self.lines.clear()
        self.im = Image.fromarray(self.nm)
        self.im_ki_copy = self.im.copy()

    def pm(self, y):
        return y + random.choice([0, 0, 0, 3, 2, 1])

    def typechars(self, typethis):
        self.im = self.im_ki_copy.copy()
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
                        return self.show_on_page()
                for k in j:
                    if k in ("f", "g", "j", "p", "q", "y"):
                        self.im.paste(
                            a := random.choice(self.d[k]),
                            (x, (slant := self.pm(slant)) + y + 8),
                            a,
                        )
                    elif k == "‘" or k == "’":
                        self.im.paste(
                            a := random.choice(self.d["'"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == ".":
                        self.im.paste(
                            a := random.choice(self.d["☺"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == ">":
                        self.im.paste(
                            a := random.choice(self.d["♥"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == "<":
                        self.im.paste(
                            a := random.choice(self.d["♦"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == "*":
                        self.im.paste(
                            a := random.choice(self.d["♠"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == ":":
                        self.im.paste(
                            a := random.choice(self.d["○"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == "/":
                        self.im.paste(
                            a := random.choice(self.d["•"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == "|":
                        self.im.paste(
                            a := random.choice(self.d["◘"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == "-" or k == "–":
                        self.im.paste(
                            a := random.choice(self.d["♣"]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    elif k == '"' or k == "“" or k == "”":
                        self.im.paste(
                            a := random.choice(self.d["☻"]),
                            (x, (slant := self.pm(slant)) + y - 8),
                            a,
                        )
                    else:
                        self.im.paste(
                            a := random.choice(self.d[k]),
                            (x, (slant := self.pm(slant)) + y),
                            a,
                        )
                    x += random.randint(15, 16)
                r = random.randint(16, 30)
                x += r
            r = random.choice([32, 36, 40])
            y += r
            y - random.randint(slant // 2, slant)
            if y > A4[1] - 50:
                return self.show_on_page()
            x = random.randint(20, 50)
            slant = 0
        # self.im.paste(self.d["ñ"][0], (A4[0]//2, 0), self.d["ñ"][0])
        self.show_on_page()

    def show_on_page(self):
        for i in self.lines:
            self.drawline(i[0], i[1])
        self.tinker_sheet_label.grid_forget()
        self.tinker_sheet = ImageTk.PhotoImage(self.im.resize(A4X))
        self.tinker_sheet_label = tk.Label(self.thekinter, image=self.tinker_sheet)
        self.tinker_sheet_label.grid(row=0, column=6, rowspan=3)

    def newpageblit(self):
        self.create_new_page()
        self.tinker_sheet_label.grid_forget()
        self.tinker_sheet = ImageTk.PhotoImage(self.im.resize(A4X))
        self.tinker_sheet_label = tk.Label(self.thekinter, image=self.tinker_sheet)
        self.tinker_sheet_label.grid(row=0, column=6, rowspan=3)

    def savefile(self, filename, filetext):
        self.im.save(f"./{filename}.png")
        with open(f"./{filename}.txt", "w") as file:
            file.write(filetext)


if __name__ == "__main__":

    root = tk.Tk()
    writer = Writer(root)
    root.configure(bg=pal.colors["temptress"])
    if os.name != "posix":
        root.iconbitmap("icon.ico")

    file_entry = tk.Entry(root, bg=pal.colors["temptress"], fg=pal.colors["wewak"])
    file_entry.grid(row=0, column=3)

    download_button = tk.Button(
        root,
        text="Download",
        bg=pal.colors["temptress"],
        fg=pal.colors["wewak"],
        command=lambda: writer.savefile(file_entry.get(), text_entry.get("1.0", "end")),
    )
    download_button.grid(row=0, column=4)

    text_entry: tk.Text = tk.Text(
        root,
        wrap=tk.WORD,
        bg=pal.colors["temptress"],
        fg=pal.colors["wewak"],
    )
    text_entry.grid(row=2, column=0, columnspan=6)

    button_process = tk.Button(
        root,
        text="Process",
        bg=pal.colors["temptress"],
        fg=pal.colors["wewak"],
        command=lambda: writer.typechars(text_entry.get("1.0", "end")),
    )
    button_process.grid(row=0, column=1)

    button_generate_new = tk.Button(
        root,
        text="Generate Sheet",
        bg=pal.colors["temptress"],
        fg=pal.colors["wewak"],
        command=writer.newpageblit,
    )
    button_generate_new.grid(row=0, column=2)

    root.mainloop()
