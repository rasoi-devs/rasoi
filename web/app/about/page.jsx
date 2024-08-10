import React from "react";
import Link from "next/link";
import Image from "next/image";
import generateMeta from "@/utils/meta";
import Markdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import styles from "./styles.module.css";

export async function generateMetadata({ params, searchParams }, parent) {
  return generateMeta("About");
}

// fetch readme from Github
async function fetchReadme() {
  const res = await fetch(
    "https://raw.githubusercontent.com/rasoi-devs/rasoi/main/README.md",
  );
  if (!res.ok) throw new Error("Failed to fetch readme");
  const content = await res.text();
  return content
    .replaceAll(
      "backend/README.md",
      "https://github.com/rasoi-devs/rasoi/tree/main/backend#readme",
    )
    .replaceAll("web/public/icon", "/icon")
    .replaceAll(
      "docs/screenshots",
      "https://raw.githubusercontent.com/rasoi-devs/rasoi/main/docs/screenshots",
    );
}

async function Page() {
  const projectReadme = await fetchReadme();

  return (
    <main>
      <Markdown
        className={styles.markdown}
        rehypePlugins={[rehypeRaw]}
        components={{
          a(props) {
            const { node, ...rest } = props;
            return (
              <Link
                target="_blank"
                className="font-medium text-blue-600 hover:underline"
                {...rest}
              />
            );
          },
          img(props) {
            const { node, ...rest } = props;
            if (props.src === "/icon-512.png")
              return (
                <Image
                  src="/icon-512.png"
                  width="64"
                  height="64"
                  alt="Rasoi Logo"
                />
              );

            return <img {...rest} />;
          },
        }}
      >
        {projectReadme}
      </Markdown>
      {/* <h1 className="mt-3 text-3xl" id="rasoi">
        Rasoi
      </h1>
      <Image src="/icon-512.png" width="64" height="64" alt="Rasoi Logo" />
      <p className="mb-3 text-justify">
        <em>A social media for recipes 🍳.</em>
      </p>
      <p className="mb-3 text-justify">
        <Link
          target="_blank"
          className="font-medium text-blue-600 hover:underline"
          href="https://www.flaticon.com/free-icon/frying-pan_1222796?term=frying+pan&amp;related_id=1222796"
        >
          Logo Source
        </Link>
      </p>
      <blockquote className="my-4 border-l-4 border-blue-400 bg-gray-200 ps-2">
        <p className="mb-3 text-justify">
          NOTE: all of the specifications given below are not finalized, may
          change if required.
        </p>
      </blockquote>
      <h2 className="mt-3 text-2xl" id="features">
        Features
      </h2>
      <ul className="list-inside list-disc space-y-1">
        <li>
          Recommended recipes (based on a recommendation engine / most popular
          rating wise).
        </li>
        <li>Search for recipes through dish name / ingredients list.</li>
        <li>Show recipe image (if possible), ratings.</li>
        <li>Comments, reactions (like, share).</li>
        <li>Posts (like Recipe images).</li>
      </ul>
      <h2 className="mt-3 text-2xl" id="future-prospects">
        Future Prospects
      </h2>
      <ul className="list-inside list-disc space-y-1">
        <li>
          We will try to detect the ingredient name from ingredient&apos;s
          image, if possible.
        </li>
        <li>
          A mobile app, possibly in{" "}
          <Link
            target="_blank"
            className="font-medium text-blue-600 hover:underline"
            href="https://flutter.dev/"
          >
            Flutter
          </Link>
          ,{" "}
          <Link
            target="_blank"
            className="font-medium text-blue-600 hover:underline"
            href="https://reactnative.dev/"
          >
            React Native
          </Link>{" "}
          or even Kotlin (native android).
        </li>
        <li>Add a post or video tutorial about the recipe.</li>
      </ul>
      <h2 className="mt-3 text-2xl" id="applications">
        Applications
      </h2>
      <ul className="list-inside list-disc space-y-1">
        <li>Cooking.</li>
        <li>Learning / Education.</li>
        <li>Social interaction.</li>
      </ul> */}
    </main>
  );
}

export default Page;
