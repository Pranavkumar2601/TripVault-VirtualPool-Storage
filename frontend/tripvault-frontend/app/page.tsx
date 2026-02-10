"use client";

import { apiFetch } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useEffect, useState } from "react";
import Link from "next/link";

export default function HomePage() {
  const { user, setUser } = useAuth();
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/users").then(setUsers).catch(console.error);
  }, []);

  function login(u: any) {
    localStorage.setItem("user_id", u.id);
    setUser(u);
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>TripVault</h1>

      {!user && (
        <>
          <h3>Select User</h3>
          {users.map((u) => (
            <div key={u.id}>
              <button onClick={() => login(u)}>
                {u.name} ({u.email})
              </button>
            </div>
          ))}
        </>
      )}

      {user && (
        <>
          <p>Logged in as: {user.name}</p>
          <Link href="/trips">Go to Trips →</Link>
        </>
      )}
    </main>
  );
}
