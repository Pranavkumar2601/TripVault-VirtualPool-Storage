"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function TripsPage() {
  const { userId } = useAuth();
  const router = useRouter();
  const [trips, setTrips] = useState<any[]>([]);
  const [name, setName] = useState("");

  useEffect(() => {
    if (!userId) {
      router.push("/login");
      return;
    }

    apiFetch("/trips").then(setTrips);
  }, [userId]);

  async function createTrip() {
    const trip = await apiFetch("/trips", {
      method: "POST",
      body: JSON.stringify({ name }),
    });

    // 🔥 IMPORTANT: redirect to trip page
    router.push(`/trips/${trip.id}`);
  }

  return (
    <div>
      <h2>My Trips</h2>

      <input
        placeholder="Trip name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={createTrip}>Create Trip</button>

      <ul>
        {trips.map((t) => (
          <li key={t.id}>
            <Link href={`/trips/${t.id}`}>{t.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
