import numpy as np

IMAGES_LOC = "dataset/archive/Food Images/Food Images"


def _load_model():
    # from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
    from keras.models import Model
    from keras.applications import MobileNetV3Small

    base_model = MobileNetV3Small(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        # optional input shape is provided, just to supress a warning
        # by default, model accepts (224, 224, 3)
        input_shape=(224, 224, 3),
    )

    # features layer should be an intermediate layer (last layer is for prediction)
    features_layer = base_model.get_layer("expanded_conv_10_project").output
    return Model(inputs=base_model.input, outputs=features_layer)


def _extract_features(image_path, model):
    # local import, to reduce mem consumption, and only load when required
    # TODO: test performance for global and local importing
    from keras.preprocessing import image
    from keras.applications.mobilenet_v3 import preprocess_input

    # model accepts input size of (224, 224, 3)
    # 3 = no. of channels, which is mostly 3 for JPEG (R, G, B)
    # TODO: try with png and transparency?
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)  # pillow image to numpy format

    # model accepts input like (1, 224, 224, 3)
    # so, add another dimension. Here 1 = batch size
    # the model can predict with multiple images at once
    # that's why we need batch size (see training part to know its use)
    # for our current use case, we are working with just 1 image
    img_array = np.expand_dims(img_array, axis=0)

    # something only the model knows...
    img_array = preprocess_input(img_array)
    features = model.predict(img_array, verbose=0)

    # we will work with features vector (1D array)
    return np.array(features.flatten()).astype("float32")


# def image_search(file_path, all_features):
# we are using pgvector, so no need to load features pkl file to
# search for images. Thus, this function is not required now
# import os
# from sklearn.metrics.pairwise import cosine_similarity

# model = _load_model()

# image_paths = [
#     f"{IMAGES_LOC}/{f}" for f in os.listdir(IMAGES_LOC) if f.endswith(".jpg")
# ]

#  query_features = _extract_features(file_path, model)
# similarities = cosine_similarity([query_features], all_features)[0]
# sorted_indices = np.argsort(similarities)[::-1]
# similar_images = [image_paths[i] for i in sorted_indices[:5]]

# del model
# del image_paths

# return similar_images


def extract_image_features(file_path):
    model = _load_model()
    return _extract_features(file_path, model)
