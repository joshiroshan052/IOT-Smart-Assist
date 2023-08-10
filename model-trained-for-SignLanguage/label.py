import os

# Define the path to the ImagePro directory
path = "ImagePro"

# Get the list of folders (sign labels) in the ImagePro directory
sign_labels = sorted(os.listdir(path))

# Create the labels.txt file
with open("labels.txt", "w") as f:
    f.write("\n".join(sign_labels))