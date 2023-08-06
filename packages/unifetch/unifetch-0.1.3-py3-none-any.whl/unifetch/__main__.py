from .ASCII_generator import img2img_color
import argparse
import os
import json


def add_name_motto(image_text: str, university: str, university_list: list) -> str:
    lines = image_text.splitlines()
    if len(lines) < 5:
        return image_text

    lines[2] = lines[2] + "\t" + ''.join([uni["fullName"] if uni["shortName"] == university else "" for uni in university_list])

    for uni in university_list:
        if uni["shortName"] == university:
            if uni["mottoTraditional"] != "":
                lines[4] = lines[3] + "\t" + uni["mottoTraditional"]
            elif uni["mottoEnglish"] != "":
                lines[4] = lines[3] + "\t" + uni["mottoEnglish"]

    return '\n'.join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="unifetch", description="Take image for processing")
    parser.add_argument("uni", nargs="?", type=str, help="University short name, for a list of universities type --show-unis")
    parser.add_argument("--num-cols", dest="num_cols", default=45, type=int, help="Width of logo in text columns")
    parser.add_argument("--show-unis", nargs="?", dest="show_unis", const=True, default=False)
    parser.add_argument("--logo-only", nargs="?", dest="logo_only", const=True, default=False)

    with open(os.path.join(os.path.dirname(__file__), "universities.json")) as f:
        universities = json.loads(f.read())
    uni_list = []
    for uni in universities:
        uni_list.append("{} - {}".format(uni["shortName"], uni["fullName"]))
    uni_list.sort()

    args = parser.parse_args()

    if args.show_unis:
        for i in uni_list:
            print(i)
        exit(0)

    if args.uni not in [uni["shortName"] for uni in universities]:
        print("University not recognised please use --show-unis to show list of universities.")
        exit(1)

    image = os.path.join(os.path.dirname(__file__), "crests", args.uni + ".png")
    image_text = img2img_color.get_text(image, num_cols=args.num_cols)
    if not args.logo_only:
        image_text = add_name_motto(image_text, args.uni, universities)
    print(image_text)
