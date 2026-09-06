import pymupdf
import json
from collections import Counter

def get_data_from_pdf(pdf):
    doc = pymupdf.open(pdf)

    all_data = []

    for page in doc:

        data = page.get_text("dict")

        parsed_data = []

        for block in data["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    parsed_data.append(
                        {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "bbox": span["bbox"],
                        }
                    )

        all_data.append(parsed_data)

    return all_data


data = get_data_from_pdf("apush_cropped.pdf")

with open("data.txt", "w") as f:
    f.write(json.dumps(data[0]))


def extract_text(pdf):

    doc = pymupdf.open(pdf)

    extracted_text = ""

    for page in doc:

        data = page.get_text("dict")

        parsed_data = []

        for block in data["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    parsed_data.append(
                        {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "bbox": span["bbox"],
                        }
                    )

        extracted_text += "".join(
            list(
                map(
                    lambda x: x["text"],
                    filter(
                        lambda x: x["size"] == 10.5 and x["color"] == 2301728,
                        parsed_data,
                    ),
                )
            )
        )

    with open("extracted.txt", "w") as file:
        file.write(extracted_text)
