import { supabase } from "./supabase.js";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiRequest(path, { method = "GET", body } = {}) {
  const { data, error } = await supabase.auth.getSession();
  let session = data?.session;
  if (error || !session) throw new Error("Authentication required");

  const makeRequest = async (accessToken) =>
    fetch(`${API_BASE}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : null,
    });

  let response = await makeRequest(session.access_token);

  if (response.status === 401) {
    const { data: refreshed, error: refreshError } = await supabase.auth.refreshSession();
    const refreshedSession = refreshed?.session;
    if (refreshError || !refreshedSession) {
      throw new Error("Invalid or expired token");
    }
    session = refreshedSession;
    response = await makeRequest(session.access_token);
  }

  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}

export const apiCall = (endpoint, method = "GET", body = null) =>
  apiRequest(endpoint, { method, body });

export const getTimetable = () => apiRequest("/api/timetable");
export const postTimetable = (data) => apiRequest("/api/timetable", { method: "POST", body: data });
