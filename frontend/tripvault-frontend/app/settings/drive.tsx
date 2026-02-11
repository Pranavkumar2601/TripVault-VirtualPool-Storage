"use client";

export default function DriveConnect() {
  const userId = localStorage.getItem("userId");

  function connect() {
    window.location.href = `${process.env.NEXT_PUBLIC_API_BASE}/auth/google/login?user_id=${userId}`;
  }

  return (
    <div>
      <h3>Google Drive</h3>
      <button onClick={connect}>Connect Google Drive</button>
    </div>
  );
}
