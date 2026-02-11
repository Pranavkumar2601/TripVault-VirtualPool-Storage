"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function InviteMember({ tripId }: { tripId: string }) {
  const [userId, setUserId] = useState("");
  const [msg, setMsg] = useState("");

  async function invite() {
    try {
      await apiFetch(`/trips/${tripId}/invite`, {
        method: "POST",
        body: JSON.stringify({ user_id: userId }),
      });
      setMsg("User invited");
      setUserId("");
    } catch (e: any) {
      setMsg(e.message);
    }
  }

  return (
    <div className="border p-3 rounded">
      <h3>Invite Member</h3>
      <input
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <button onClick={invite}>Invite</button>
      <p>{msg}</p>
    </div>
  );
}
