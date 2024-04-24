import os
import tensorflow as tf
from keras.applications import MobileNetV3Small


IMAGES_DIR = "/media/tom/OS/images"

urls = [f"{IMAGES_DIR}/{f}" for f in os.listdir(IMAGES_DIR)]
batch_size = 16
n_batches = len(urls) // batch_size


def load_img(url):
    image = tf.read_file(url, name="image_data")
    image = tf.image.decode_jpeg(image, channels=3, name="image")
    return image


def preprocess(img_tensor):
    img_tensor = (tf.cast(img_tensor, tf.float32) / 255 - 0.5) * 2
    img_tensor.set_shape((224, 224, 3))
    return img_tensor


dataset = tf.contrib.data.Dataset.from_tensor_slices(urls)
dataset = dataset.map(load_img).map(preprocess)

preprocessed_images = dataset.batch(batch_size).make_one_shot_iterator().get_next()


model = MobileNetV3Small(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    # input shape is provided, just to suppress a warning
    input_shape=(224, 224, 3),
)
model.trainable = False
# TODO: exct layer
output = model(preprocessed_images, training=False)


results = []

with tf.Session() as sess:
    tf.train.Saver().restore(sess, "checkpoint_file.txt")
    for i in range(n_batches):
        batch_results = sess.run(output)
        results.extend(batch_results)
        print("Done batch %d / %d" % (i + 1, n_batches))
