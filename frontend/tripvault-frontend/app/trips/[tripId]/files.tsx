"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function Files({ tripId }: { tripId: string }) {
  const [files, setFiles] = useState<any[]>([]);
  const [file, setFile] = useState<File | null>(null);

  async function load() {
    const data = await apiFetch(`/files?trip_id=${tripId}`);
    setFiles(data);
  }

  useEffect(() => {
    load();
    const i = setInterval(load, 3000); // status polling
    return () => clearInterval(i);
  }, []);

  async function upload() {
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE}/files/upload-and-store?trip_id=${tripId}`,
      {
        method: "POST",
        headers: {
          "X-User-ID": localStorage.getItem("userId")!,
        },
        body: form,
      },
    );

    setFile(null);
    load();
  }

  return (
    <div>
      <h3>Files</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={upload}>Upload</button>

      <ul>
        {files.map((f) => (
          <li key={f.id}>
            {f.path} — {f.status} — {f.progress_percent}%
            {f.status === "completed" && (
              <a
                href={`${process.env.NEXT_PUBLIC_API_BASE}/files/${f.id}/download`}
                target="_blank"
              >
                Download
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
