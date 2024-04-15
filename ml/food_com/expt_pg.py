import matplotlib.pyplot as plt
from pgvector.psycopg import register_vector
import psycopg
import tempfile
import torch
import torchvision
from tqdm import tqdm
import os
from torch.utils.data import Dataset
from torchvision.io import read_image
from PIL import Image


class CustomImageDataset(Dataset):
    def __init__(
        self,
        img_dir,
        transform=None,
        # target_transform=None,
    ):
        self.img_dir = img_dir
        self.files = [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)[:1000]
            if f.endswith(".jpg")
        ]
        self.transform = transform
        # self.target_transform = target_transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        image = read_image(self.files[idx])
        # label = self.img_labels.iloc[idx, 1]
        if self.transform:
            if isinstance(image, torch.Tensor):
                image = torchvision.transforms.ToPILImage()(image)
                image = image.convert("RGB")
                image = self.transform(image)
        # if self.target_transform:
        #     label = self.target_transform(label)
        # return image, label
        return image


seed = True

# establish connection
conn = psycopg.connect(
    conninfo="host=localhost port=5432 user=postgres dbname=rasoi2 password=password",
    autocommit=True,
)
conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)

# load images
transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.Resize((224, 224)),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)
# dataset = torchvision.datasets.CIFAR10(
#     root=tempfile.gettempdir(), train=True, download=True, transform=transform
# )
dataset = CustomImageDataset(img_dir="/media/tom/OS/images", transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=2)

# load pretrained model
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = torchvision.models.resnet18(weights="DEFAULT")
model.fc = torch.nn.Identity()
model.to(device)
model.eval()


def generate_embeddings(inputs):
    return model(inputs.to(device)).detach().cpu().numpy()


# generate and store embeddings
if seed:
    conn.execute("DROP TABLE IF EXISTS image")
    conn.execute("CREATE TABLE image (id bigserial PRIMARY KEY, embedding vector(512))")

    print("Generating embeddings")
    for data in tqdm(dataloader):
        # embeddings = generate_embeddings(data[0])
        embeddings = generate_embeddings(data)

        sql = "INSERT INTO image (embedding) VALUES " + ",".join(
            ["(%s)" for _ in embeddings]
        )
        params = [embedding for embedding in embeddings]
        conn.execute(sql, params)

# load 5 random unseen images
# queryset = torchvision.datasets.CIFAR10(
#     root=tempfile.gettempdir(), train=False, download=True, transform=transform
# )
queryset = CustomImageDataset(img_dir="/media/tom/OS/images", transform=transform)
queryloader = torch.utils.data.DataLoader(queryset, batch_size=5, shuffle=True)
images = next(iter(queryloader))[0]
# images = [
#     "/media/tom/OS/images/recipe_369780_1.jpg",
#     "/media/tom/OS/images/recipe_369741_0.jpg",
# ]

# generate and query embeddings
results = []
# embeddings = generate_embeddings(images)
print("emb strt")
embeddings = []
for image in queryloader:
    embeddings.append(generate_embeddings(image))
print("emb done")
for image, embedding in zip(images, embeddings):
    result = conn.execute(
        "SELECT id FROM image ORDER BY embedding <=> %s LIMIT 5", (embedding,)
    ).fetchall()
    nearest_images = [dataset[row[0] - 1][0] for row in result]
    results.append([image] + nearest_images)

# show images
fig, axs = plt.subplots(len(results), len(results[0]))
for i, result in enumerate(results):
    for j, image in enumerate(result):
        ax = axs[i, j]
        ax.imshow((image / 2 + 0.5).permute(1, 2, 0).numpy())
        ax.set_axis_off()
plt.show(block=True)
