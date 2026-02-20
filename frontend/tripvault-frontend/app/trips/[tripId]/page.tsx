"use client";

import { useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api, apiRequest } from "@/lib/api";

type Member = {
  id: string;
  user_id: string;
  role: string;
  allocated_bytes: number;
  used_bytes: number;
};

type Trip = {
  id: string;
  name: string;
  created_by: string;
  members: Member[];
};

type FileItem = {
  id: string;
  path: string;
  status: string;
  uploaded_bytes: number;
  size_bytes: number;
  progress_percent: number;
};

export default function TripDetailPage() {
  const { tripId } = useParams<{ tripId: string }>();
  const router = useRouter();

  const [trip, setTrip] = useState<Trip | null>(null);
  const [files, setFiles] = useState<FileItem[]>([]);
  const [quota, setQuota] = useState("");
  const [driveConnected, setDriveConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const pollingRefs = useRef<Record<string, NodeJS.Timeout>>({});

  // -------------------------
  // Initial Load
  // -------------------------
  useEffect(() => {
    loadData();
  }, []);

  // Cleanup intervals
  useEffect(() => {
    return () => {
      Object.values(pollingRefs.current).forEach(clearInterval);
    };
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const trips = await api.get<Trip[]>("/trips");
      const found = trips.find((t) => t.id === tripId);

      if (!found) {
        setError("Trip not found");
        return;
      }

      setTrip(found);

      const fileData = await api.get<FileItem[]>(`/files?trip_id=${tripId}`);
      setFiles(fileData);

      const drive = await api.get<{
        connected: boolean;
      }>("/auth/google/status");

      setDriveConnected(drive.connected);

      fileData.forEach((f) => {
        if (f.status === "uploading" || f.status === "pending") {
          startPolling(f.id);
        }
      });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // -------------------------
  // Polling
  // -------------------------
  const startPolling = (fileId: string) => {
    if (pollingRefs.current[fileId]) return;

    const interval = setInterval(async () => {
      try {
        const status = await api.get<{
          status: string;
          progress_percent: number;
          uploaded_bytes: number;
          size_bytes: number;
        }>(`/files/${fileId}/status`);

        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileId
              ? {
                  ...f,
                  ...status,
                }
              : f,
          ),
        );

        if (status.status === "completed" || status.status === "failed") {
          clearInterval(pollingRefs.current[fileId]);
          delete pollingRefs.current[fileId];
        }
      } catch {
        clearInterval(pollingRefs.current[fileId]);
        delete pollingRefs.current[fileId];
      }
    }, 5000);

    pollingRefs.current[fileId] = interval;
  };

  // -------------------------
  // Upload
  // -------------------------
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!driveConnected) {
      alert("Connect Google Drive first");
      return;
    }

    if (!e.target.files?.length) return;

    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const data = await apiRequest<{
        virtual_file_id: string;
      }>(`/files/upload-and-store?trip_id=${tripId}`, {
        method: "POST",
        body: formData,
      });

      await loadData();
      startPolling(data.virtual_file_id);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const deleteFile = async (id: string) => {
    await api.delete(`/files/${id}`);
    loadData();
  };

  const updateQuota = async () => {
    if (!quota.trim()) return;

    await api.patch(`/trips/${tripId}/me/quota?allocated_bytes=${quota}`);

    setQuota("");
    loadData();
  };

  if (loading) return <div className="p-8">Loading...</div>;

  if (error || !trip) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div className="p-8 space-y-8">
      <button
        onClick={() => router.push("/trips")}
        className="text-sm text-blue-600"
      >
        ← Back
      </button>

      <h1 className="text-2xl font-bold">{trip.name}</h1>

      {/* Drive Status */}
      <div className="border p-4 rounded">
        <h2 className="font-semibold mb-2">Google Drive</h2>

        {driveConnected ? (
          <div className="text-green-600 text-sm">Connected</div>
        ) : (
          <div className="space-y-2">
            <div className="text-red-600 text-sm">Not connected</div>
            <button
              onClick={() => {
                const userId = localStorage.getItem("tv_user_id");
                window.location.href = `http://localhost:8000/api/v1/auth/google/login?user_id=${userId}`;
              }}
              className="bg-black text-white px-3 py-1 rounded text-sm"
            >
              Connect Drive
            </button>
          </div>
        )}
      </div>

      {/* Members */}
      <div className="border p-4 rounded">
        <h2 className="font-semibold mb-2">Members ({trip.members.length})</h2>

        {trip.members.map((m) => (
          <div key={m.id} className="flex justify-between text-sm">
            <span>
              {m.user_id} ({m.role})
            </span>
            <span>
              {m.used_bytes} / {m.allocated_bytes}
            </span>
          </div>
        ))}

        <div className="mt-4 flex gap-2">
          <input
            value={quota}
            onChange={(e) => setQuota(e.target.value)}
            placeholder="Set my quota (bytes)"
            className="border px-2 py-1 rounded"
          />
          <button
            onClick={updateQuota}
            className="bg-black text-white px-3 rounded"
          >
            Update
          </button>
        </div>
      </div>

      {/* Upload */}
      <div className="border p-4 rounded">
        <h2 className="font-semibold mb-3">Upload</h2>
        <input type="file" onChange={handleUpload} />
      </div>

      {/* Files */}
      <div className="border p-4 rounded">
        <h2 className="font-semibold mb-3">Files</h2>

        {files.map((f) => (
          <div key={f.id} className="border p-3 rounded mb-3">
            <div className="font-medium">{f.path}</div>

            <div className="text-xs text-gray-500 mb-1">
              {f.status} — {f.progress_percent}%
            </div>

            <div className="w-56 bg-gray-200 h-2 rounded mb-2">
              <div
                className="bg-green-600 h-2 rounded transition-all"
                style={{
                  width: `${f.progress_percent}%`,
                }}
              />
            </div>

            <div className="flex gap-3 text-sm">
              <a
                href={`http://localhost:8000/api/v1/files/${f.id}/download`}
                target="_blank"
                className="text-blue-600"
              >
                Download
              </a>
              <button onClick={() => deleteFile(f.id)} className="text-red-600">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
