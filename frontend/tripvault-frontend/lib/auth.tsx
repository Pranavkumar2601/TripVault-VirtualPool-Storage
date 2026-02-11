"use client";

import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext<any>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("userId");
    if (saved) setUserId(saved);
  }, []);

  function login(id: string) {
    localStorage.setItem("userId", id);
    setUserId(id);
  }

  function logout() {
    localStorage.removeItem("userId");
    setUserId(null);
  }

  return (
    <AuthContext.Provider value={{ userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
