export function setUserId(id: string) {
  localStorage.setItem("tv_user_id", id);
}

export function getUserId(): string | null {
  return localStorage.getItem("tv_user_id");
}

export function clearUserId() {
  localStorage.removeItem("tv_user_id");
}
