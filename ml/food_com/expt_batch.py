import tensorflow as tf
import numpy as np
import os, pickle
from datetime import datetime
from keras.models import Model

# from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from keras.applications import MobileNetV3Small
from keras.applications.mobilenet_v3 import preprocess_input
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import BallTree

# model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# NOTE: mobilenet is faster
base_model = MobileNetV3Small(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    # input shape is provided, just to suppress a warning
    input_shape=(224, 224, 3),
)

# Remove the last layer (classification layer)
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)


# Directory containing images
image_folder = "/media/tom/OS/images"
query_image_path = "/media/tom/OS/images/recipe_76_8.jpg"


# Define batch size
BATCH_SIZE = 512

# Create empty lists to store features and image paths
all_features = []
all_image_paths = []


def extract_features_batch(image_paths):
    batch_features = []
    batch_images = []
    for image_path in image_paths:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        batch_images.append(img_array)

    batch_images = np.vstack(batch_images)
    features = model.predict(batch_images, batch_size=BATCH_SIZE)
    # features = features.reshape((features.shape[0], 7 * 7 * 2048))
    for feature in features:
        batch_features.append(feature.flatten())
    return np.array(batch_features).astype("float32")


image_paths = [
    f"{image_folder}/{f}" for f in os.listdir(image_folder) if f.endswith(".jpg")
][:10000]

for i in range(0, len(image_paths), BATCH_SIZE):
    batch_image_paths = []
    for path in image_paths[i : i + BATCH_SIZE]:
        batch_image_paths.append(path)
    batch_features = extract_features_batch(batch_image_paths)
    all_features.extend(batch_features)

all_features = np.array(all_features)

# Build BallTree index
tree = BallTree(all_features, leaf_size=40)

query_features = extract_features_batch([query_image_path])

k = 5
distances, indices = tree.query(query_features, k=k)
top_similar_images = [image_paths[i] for i in indices[0]]
print(f"Top 5 similar images for {query_image_path}:")
for image_path in top_similar_images:
    print(image_path)


# timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
# index_file = f"dataset/balltree_index_{timestamp}.pkl"
# with open(index_file, "wb") as f:
#     pickle.dump(tree, f)

# print("BallTree index saved to:", index_file)

timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
features_file = f"dataset/features_{timestamp}.pkl"
with open(features_file, "wb") as f:
    pickle.dump(all_features, f)

print("all features saved to:", features_file)
