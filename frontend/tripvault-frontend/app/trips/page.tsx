"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

type Trip = {
  id: string;
  name: string;
  created_by: string;
};

export default function TripsPage() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  const loadTrips = async () => {
    try {
      const data = await api.get<Trip[]>("/trips");
      setTrips(data);
    } catch (err: any) {
      setError(err.message || "Failed to load trips");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const userId = localStorage.getItem("tv_user_id");
    if (!userId) {
      router.push("/");
      return;
    }

    loadTrips();
  }, []);

  const createTrip = async () => {
    if (!name.trim()) return;

    try {
      await api.post("/trips", { name });
      setName("");
      loadTrips();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) {
    return <div className="p-8">Loading trips...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-600">Error: {error}</div>;
  }

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">My Trips</h1>

      <div className="flex gap-2 mb-6">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Trip name"
          className="border px-3 py-2 rounded w-full"
        />
        <button
          onClick={createTrip}
          className="bg-black text-white px-4 rounded"
        >
          Create
        </button>
      </div>

      <div className="space-y-3">
        {trips.map((trip) => (
          <div
            key={trip.id}
            className="border p-4 rounded cursor-pointer hover:bg-gray-50"
            onClick={() => router.push(`/trips/${trip.id}`)}
          >
            {trip.name}
          </div>
        ))}

        {trips.length === 0 && (
          <div className="text-sm text-gray-500">No trips yet.</div>
        )}
      </div>
    </div>
  );
}
