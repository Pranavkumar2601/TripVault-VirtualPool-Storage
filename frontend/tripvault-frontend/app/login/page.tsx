"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [users, setUsers] = useState<any[]>([]);
  const { login } = useAuth();
  const router = useRouter();

  useEffect(() => {
    apiFetch("/users").then(setUsers);
  }, []);

  function selectUser(id: string) {
    login(id);
    router.push("/trips");
  }

  return (
    <div>
      <h2>Select User</h2>
      {users.map((u) => (
        <button key={u.id} onClick={() => selectUser(u.id)}>
          {u.email}
        </button>
      ))}
    </div>
  );
}

// "use client";

// import { useEffect, useState } from "react";
// import { apiFetch } from "@/lib/api";
// import { useAuth } from "@/lib/auth";
// import { useRouter } from "next/navigation";

// export default function LoginPage() {
//   const [users, setUsers] = useState<any[]>([]);
//   const { login } = useAuth();
//   const router = useRouter();

//   useEffect(() => {
//     apiFetch("/users").then(setUsers);
//   }, []);

//   function selectUser(id: string) {
//     login(id);
//     router.push("/trips");
//   }

//   return (
//     <div>
//       <h2>Select User</h2>
//       {users.map((u) => (
//         <button key={u.id} onClick={() => selectUser(u.id)}>
//           {u.email}
//         </button>
//       ))}
//     </div>
//   );
// }
