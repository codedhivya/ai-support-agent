"use client";

import { useState } from "react";
import { uploadDocument } from "@/services/document";

export default function UploadDocument() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    try {
      setLoading(true);

      const result = await uploadDocument(file);

      console.log(result);

      alert("File uploaded successfully");
      window.location.reload();

      setFile(null);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="mb-4">
        <input
          type="file"
          accept=".pdf,.txt,.doc,.docx"
          className="border p-3 rounded w-full"
          onChange={(e) => {
            const selectedFile = e.target.files?.[0] || null;

            console.log("Selected file:", selectedFile);

            setFile(selectedFile);
          }}
        />
      </div>

      {file && (
        <div className="mb-4">
          Selected File: <b>{file.name}</b>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? "Uploading..." : "Upload Document"}
      </button>
    </div>
  );
}
