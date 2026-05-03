"""
Generates an HTML file that acts like
a PowerPoint containing only videos from
a manim-slides project.
JSON-file must be called data.json.
"""

import json
import base64
import os
import sys

SOURCE_PATH = "source"
OUT_PATH = "out"


class Generator:
    def __init__(self, name: str):
        if not os.path.exists("source"):
            os.mkdir("source")
            raise BaseException("Put your slides folder in the source directory!")

        self.name = name
        self.source_path = SOURCE_PATH + "/" + name

        files = os.listdir(self.source_path)
        data_file = None
        for f in files:
            if f.endswith(".json"): data_file = f

        if data_file is None:
            raise BaseException("File couldn't be found!")

        with open(self.source_path + "/" + data_file, "r") as file:
            self.source_data = json.loads(file.read())

        with open("template/index.html", "r") as file:
            self.out = file.read()

    def gen(self):
        sources = "["

        for slide in self.source_data["slides"]:
            rel_path = slide["file"].removeprefix("slides/")
            full_path = f"{self.source_path}/{rel_path}"

            with open(full_path, "rb") as file:
                data = base64.b64encode(file.read()).decode("utf-8")

            sources += f"\n\t`data:video/mp4;base64,{data.replace("\n", "")}`,"

        sources += "\n]"
        self.out = self.out.replace("[[__SOURCES__]]", sources)

    def save(self):
        out_folder = OUT_PATH + "/" + self.name

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        with open(out_folder + "/index.html", "w") as file:
            print(self.out)
            file.write(self.out)


if __name__ == "__main__":
    gen = Generator(sys.argv[1])
    gen.gen()
    gen.save()