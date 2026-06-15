import UploadDocument from "@/components/UploadDocument";

import DocumentList from "@/components/DocumentList";

import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">AI Support Agent</h1>

        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded shadow">
            <UploadDocument />
          </div>

          <div className="bg-white p-6 rounded shadow">
            <DocumentList />
          </div>

          <Link
            href="/chat"
            className="bg-green-600 text-white px-4 py-2 rounded inline-block mt-4"
          >
            Open Chat Assistant
          </Link>
        </div>
      </div>
    </div>
  );
}
