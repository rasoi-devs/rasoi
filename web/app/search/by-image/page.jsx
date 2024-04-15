"use client";

import React, { useCallback, useRef, useState } from "react";
import { toast } from "react-toastify";
import RecipeList from "@/components/RecipeList";
import { useDropzone } from "react-dropzone";

const MAX_FILE_SIZE = 3_000_000; // mb in bytes

function SearchByImage() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [emptyMessage, setEmptyMessage] = useState("Drop / pick an image...");

  const onDrop = useCallback((acceptedFiles) => {
    const data = new FormData();
    setSelectedImage(acceptedFiles[0]);
    data.append("image_file", acceptedFiles[0]);
    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/recipes-from-image`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        // "Content-Type": "multipart/form-data",
      },
      body: data,
    })
      .then((res) => res.json())
      .then((recipesJson) => {
        setRecipes(recipesJson);
        if (recipesJson.length === 0) setEmptyMessage("No results found!");
      })
      .catch((_) => toast.error("You might be offline!"))
      .finally(() => setLoading(false));
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    autoFocus: true,
    maxFiles: 1,
    maxSize: MAX_FILE_SIZE,
    accept: {
      // TODO: try with transparent png
      "image/*": [".png", ".jpeg", ".jpg"],
    },
    multiple: false,
  });

  return (
    <main className="flex flex-1 flex-col">
      <div
        {...getRootProps()}
        className="flex flex-1 flex-col items-center justify-center rounded-lg border-2 border-dashed border-primary-500 text-center text-2xl outline-none focus:border-4"
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the file here...</p>
        ) : (
          <p className="zoomInOut">
            Drag &apos;n&apos; drop an image, or click to pick a file
          </p>
        )}
      </div>

      {selectedImage && (
        <div className="mt-2 flex flex-col items-center justify-center gap-2 text-xl">
          <img
            className="h-32 rounded-xl object-cover"
            src={URL.createObjectURL(selectedImage)}
            alt={selectedImage.name}
          />
          <span>{selectedImage.name}</span>
        </div>
      )}

      <div className="p-2"></div>

      <RecipeList
        recipes={recipes}
        skeleton={loading}
        emptyText={emptyMessage}
      />
    </main>
  );
}

export default SearchByImage;
