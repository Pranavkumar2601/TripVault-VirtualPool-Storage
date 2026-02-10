"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function TripsPage() {
  const { user } = useAuth();
  const [trips, setTrips] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadTrips() {
    try {
      const data = await apiFetch("/trips");
      setTrips(data);
    } catch (e: any) {
      setError(e.message);
    }
  }

  useEffect(() => {
    if (user) loadTrips();
  }, [user]);

  async function createTrip(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;

    try {
      setLoading(true);
      setError(null);

      await apiFetch("/trips", {
        method: "POST",
        body: JSON.stringify({ name }),
      });

      setName("");
      await loadTrips(); // refresh list
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  if (!user) return <p>Please login first</p>;

  return (
    <main style={{ padding: 24, maxWidth: 600 }}>
      <h1>My Trips</h1>

      {/* Create Trip */}
      <form onSubmit={createTrip} style={{ marginBottom: 24 }}>
        <h3>Create New Trip</h3>

        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Trip name"
          style={{ padding: 8, width: "100%" }}
        />

        <button type="submit" disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Creating..." : "Create Trip"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Trips List */}
      {trips.length === 0 && <p>No trips yet</p>}

      {trips.map((t) => (
        <div
          key={t.id}
          style={{
            padding: 12,
            border: "1px solid #ccc",
            marginBottom: 8,
          }}
        >
          <strong>{t.name}</strong>
          <div style={{ fontSize: 12 }}>Trip ID: {t.id}</div>
        </div>
      ))}
    </main>
  );
}
