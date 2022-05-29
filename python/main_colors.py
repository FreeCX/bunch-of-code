from sklearn.cluster import KMeans
from PIL import Image, ImageDraw
from os.path import splitext
import colorsys as cs
import math


def get_main_colors(filename, n_colors=5, debug_image=False, use_hsv=True):
    img = Image.open(filename).convert("RGB")
    if img.size[0] != img.size[1]:
        div = math.gcd(img.size[0], img.size[1])
    else:
        div = math.gcd(img.size[0], 5)
    new_size = (img.size[0] // div, img.size[1] // div)
    img = img.resize(new_size, Image.NEAREST)

    if use_hsv:
        x_data = [cs.rgb_to_hsv(*x) for x in set(img.getdata())]
    else:
        x_data = list(set(img.getdata()))

    labels = KMeans(n_clusters=n_colors, random_state=0).fit_predict(x_data)
    labels_count = len(set(labels))
    clusters = [[] for _ in range(labels_count)]
    for item, label in zip(x_data, labels):
        clusters[label].append(item)
    clusters.sort()

    result_colors = []
    for line in clusters:
        if use_hsv:
            color = tuple(map(math.ceil, cs.hsv_to_rgb(*line[0])))
            result_colors.append(color)
        else:
            result_colors.append(line[0])

    if debug_image:
        img_name = splitext(filename)[0]
        img = Image.new("RGB", (labels_count, 1))
        draw = ImageDraw.Draw(img)
        for x, color in enumerate(result_colors):
            draw.point((x, 0), color)
        del draw
        img = img.resize((64 * labels_count, 64), Image.NEAREST)
        debug_image_name = "{}-colors.png".format(img_name)
        img.save(debug_image_name)
        print("> `{}` succesfully created!".format(debug_image_name))

    return result_colors


if __name__ == "__main__":
    for image in ["01.jpg", "02.jpg"]:
        cl = get_main_colors(image, debug_image=True, n_colors=7)
        print(f"{image}: {cl}")
