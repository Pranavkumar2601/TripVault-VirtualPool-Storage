"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function DriveSettingsPage() {
  const [connected, setConnected] = useState<boolean | null>(null);

  useEffect(() => {
    apiFetch("/auth/google/status")
      .then((res) => setConnected(res.connected))
      .catch(() => setConnected(false));
  }, []);

  if (connected === null) {
    return <p>Checking Drive status…</p>;
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Google Drive</h1>

      {connected ? (
        <p style={{ color: "green" }}>✅ Google Drive connected</p>
      ) : (
        <a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/google/login`}>
          <button>Connect Google Drive</button>
        </a>
      )}
    </div>
  );
}
