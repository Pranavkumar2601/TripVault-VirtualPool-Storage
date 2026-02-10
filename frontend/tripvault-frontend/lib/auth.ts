export function getCurrentUserId() {
  return localStorage.getItem("user_id");
}

export function setCurrentUserId(id: string) {
  localStorage.setItem("user_id", id);
}
