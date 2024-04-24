import tensorflow as tf
import numpy as np
import os, pickle
from datetime import datetime

# from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from keras.applications import MobileNetV3Small
from keras.applications.mobilenet_v3 import preprocess_input
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import BallTree

# model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# NOTE: mobilenet is faster
model = MobileNetV3Small(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    # input shape is provided, just to suppress a warning
    input_shape=(224, 224, 3),
)


# Function to extract features from an image
def extract_features(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()


# Function to calculate cosine similarity between two feature vectors
def calculate_similarity(query_features, all_features):
    similarities = cosine_similarity(query_features, all_features)
    return similarities[0]


# Directory containing images
image_folder = "/media/tom/OS/images"
query_image_path = "/media/tom/OS/images/recipe_76_8.jpg"

# Extract features from query image
query_features = extract_features(query_image_path)

# Extract features from all images in the folder
all_features = []
all_image_paths = []
for filename in os.listdir(image_folder)[:1000]:
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_folder, filename)
        all_image_paths.append(image_path)
        features = extract_features(image_path)
        all_features.append(features)

# Convert feature vectors to numpy array
all_features = np.array(all_features).astype("float32")

# Build BallTree index
tree = BallTree(all_features, leaf_size=40)

# Perform similarity search
k = 5  # Number of nearest neighbors to retrieve
distances, indices = tree.query([query_features], k=k)

# Retrieve paths of similar images
top_similar_images = [all_image_paths[i] for i in indices[0]]

print(f"Top 5 similar images for {query_image_path}:")
for image_path in top_similar_images:
    print(image_path)

# Generate timestamp
timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

# Save the BallTree index to a file with timestamp
index_file = f"dataset/balltree_index_{timestamp}.pkl"
with open(index_file, "wb") as f:
    pickle.dump(tree, f)

print("BallTree index saved to:", index_file)

# Calculate similarity between query image and all other images
similarities = calculate_similarity([query_features], all_features)

# Sort images based on similarity
sorted_indices = np.argsort(similarities)[::-1]

# Return top 5 similar images
top_similar_images = [all_image_paths[i] for i in sorted_indices[:5]]

print(f"Top 5 similar (cosine) images for {query_image_path}:")
for image_path in top_similar_images:
    print(image_path)
