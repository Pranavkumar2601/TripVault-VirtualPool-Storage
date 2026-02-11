"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function Quota({ tripId }: { tripId: string }) {
  const [bytes, setBytes] = useState("");
  const [msg, setMsg] = useState("");

  async function updateQuota() {
    try {
      await apiFetch(`/trips/${tripId}/me/quota?allocated_bytes=${bytes}`, {
        method: "PATCH",
      });
      setMsg("Quota updated successfully");
    } catch (e: any) {
      setMsg(e.message);
    }
  }

  return (
    <div className="border p-3 rounded">
      <h3>My Storage Contribution</h3>

      <input
        type="number"
        placeholder="Bytes (eg: 10737418240 = 10GB)"
        value={bytes}
        onChange={(e) => setBytes(e.target.value)}
      />

      <button onClick={updateQuota}>Update</button>

      <p>{msg}</p>
    </div>
  );
}
