#!/usr/bin/env python3

from tkinter import Tk, Text, Label, DISABLED, END, WORD
import json

RESULT_TAG = "RESULT_TAG"
data_name = "sid2005"
json_file = "{}.json".format(data_name)

data = {
"special_char" : 's',
"classes": {"p": "Eiendomsord bak substantiv",
"u": "Uttrykk der eiendomsord er foran",
"t": "Trykk på eiendomsord => foran",
"c": "Eiendomsord foran, høres best ut slik",
"z": "Eiendomsord kunne vært bak",
"x": "Eiendomsord burde vært bak",
"i": "ingen substantiv",
" ": "ikke eiendomsord"},
"search_str": r"\y(min|mi|mitt|mine|din|di|ditt|dine|sin|sitt|sine|hans|hennes|dens|dets|vår|vårt|våre|deres|dems)\y", #Tcl word boundry
"text_pos": "0.0",
"special": False,
"kommentar": "Vi driter i å matche 'si'"
}
data["registered"] = {class_name:[] for class_name in data["classes"].values()}

try:
    with open(json_file) as infile:
        data = json.load(infile)
except FileNotFoundError:
    pass

def main():
    with open("{}.txt".format(data_name), encoding='utf-8') as o:
        all_text = ''.join(o.readlines())

    root = Tk()

    text = Text(root, width=80, height=40, wrap=WORD)
    text.pack()

    label = Label(root, text="LABEL")
    label.pack()

    text.insert(END, all_text)
    text.config(state=DISABLED)
    text.tag_config(RESULT_TAG, background="yellow", foreground="black")

    def update_label():
        text = "{}\n Found at: {}\n".format(data["search_str"], data["text_pos"])
        for key,class_name in data["classes"].items():
            text += "'{}' - {}: {}\n".format(key, class_name, len(data["registered"][class_name]))
        text += "\n{} - {}".format(data["special_char"], "UNSPECIAL" if data["special"] else "special")
        label.config(text=text)

    update_label()

    def next_word(move=True):
        if not data["text_pos"]:
            return
        text.tag_remove(RESULT_TAG, "1.0", END)

        pos = data["text_pos"]
        if move or pos=="0.0":
            pos = text.search(data["search_str"], pos+"+1c", stopindex=END, regexp=True, nocase=True) #We need stopindex to not wrap search

        if pos:
            text.see(pos)
            text.tag_add(RESULT_TAG, pos, "{} wordend".format(pos))

        data["text_pos"] = pos
        data["special"] = False
        update_label()

    def keypress(event):
        c = event.char
        if c == data["special_char"]:
            data["special"] = not data["special"]
            update_label()
        elif c in data["classes"] and data["text_pos"] is not None:
            data["registered"][data["classes"][c]].append({"pos": data["text_pos"], "special": data["special"]})
            next_word()

    root.bind('<Key>', keypress)

    next_word(False)
    root.mainloop()

    with open(json_file, "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
