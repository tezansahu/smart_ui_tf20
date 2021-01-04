from bs4 import BeautifulSoup
from imutils import paths
import os
import pandas as pd
import cv2

snip_root_dir = "./snipped"
annot_path = "./annotations_v1"
images_path = "./images"
data_csv = "./component_data.csv"
classes_csv = "./classes.csv"

def createBoundingBoxesData():
    # grab all image paths then construct the training and testing split
    imagePaths = list(paths.list_files(images_path))

    # create the list of datasets to build
    dataset = [("dataset", imagePaths, data_csv)]

    # initialize the set of classes we have
    CLASSES = set()

    # loop over the datasets
    for (dType, imagePaths, outputCSV) in dataset:
        # load the contents
        print ("[INFO] creating '{}' set...".format(dType))
        print ("[INFO] {} total images in '{}' set".format(len(imagePaths), dType))

        # open the output CSV file
        csv = open(outputCSV, "w")

        # loop over the image paths
        for imagePath in imagePaths:
            # build the corresponding annotation path
            fname = imagePath.split(os.path.sep)[-1]
            fname = "{}.json".format(fname[:fname.rfind(".")])
            annotPath = os.path.sep.join([annot_path, fname])

            # load the contents of the annotation file and buid the soup
            contents = open(annotPath).read()
            soup = BeautifulSoup(contents, "html.parser")

            # extract the image dimensions
            w = int(soup.find("width").string)
            h = int(soup.find("height").string)

            # loop over all object elements
            for o in soup.find_all("object"):
                #extract the label and bounding box coordinates
                label = o.find("name").string
                xMin = int(float(o.find("xmin").string))
                yMin = int(float(o.find("ymin").string))
                xMax = int(float(o.find("xmax").string))
                yMax = int(float(o.find("ymax").string))

                # truncate any bounding box coordinates that fall outside
                # the boundaries of the image
                xMin = max(0, xMin)
                yMin = max(0, yMin)
                xMax = min(w, xMax)
                yMax = min(h, yMax)

                # ignore the bounding boxes where the minimum values are larger
                # than the maximum values and vice-versa due to annotation errors
                if xMin >= xMax or yMin >= yMax:
                    continue
                elif xMax <= xMin or yMax <= yMin:
                    continue

                # write the image path, bounding box coordinates, label to the output CSV
                row = [os.path.abspath(imagePath),str(xMin), str(yMin), str(xMax),
                        str(yMax), str(label)]
                csv.write("{}\n".format(",".join(row)))

                # update the set of unique class labels
                CLASSES.add(label)

        # close the CSV file
        csv.close()

    # write the classes to file
    print("[INFO] writing classes...")
    csv = open(classes_csv, "w")
    rows = [",".join([c, str(i)]) for (i,c) in enumerate(CLASSES)]
    csv.write("\n".join(rows))
    csv.close()


def createClassDir(snip_root_dir, class_label):
    os.makedirs(os.path.join(snip_root_dir, class_label), exist_ok=True)

def rowToSnip(row):
    im = cv2.imread(row["img_path"])
    extracted = im[row["ymin"]:row["ymax"], row["xmin"]:row["xmax"]]

    cv2.imwrite(os.path.join(snip_root_dir, row["class"], f"{row.name}.png"), extracted)

def imagesToSnips(annot_df, classes_df):
    print("[INFO] snipping components...")
    classes_df.apply(lambda s: createClassDir(snip_root_dir, s["class_name"]), axis=1)
    annot_df.apply(rowToSnip, axis=1)


def main():
    createBoundingBoxesData()

    classes_df = pd.read_csv(classes_csv, header=None, names=["class_name", "class_label"])
    data_df = pd.read_csv(data_csv, header=None, names=["img_path", "xmin", "ymin", "xmax", "ymax", "class"])

    imagesToSnips(data_df, classes_df)

if __name__ == "__main__":
    main()