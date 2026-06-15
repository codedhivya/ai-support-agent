"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "@/services/document";

export default function DocumentList() {
  const [documents, setDocuments] = useState<any[]>([]);

  useEffect(() => {
    loadDocuments();
  }, []);

   const loadDocuments = async () => {
    try {
      const data = await getDocuments();

      setDocuments(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Uploaded Documents</h2>

      <div className="space-y-2">
        {documents.map((doc) => (
          <div key={doc.id} className="border rounded p-3">
            {doc.file_name}
          </div>
        ))}
      </div>
    </div>
  );
}
