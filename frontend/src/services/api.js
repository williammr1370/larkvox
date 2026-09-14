/**
 * Cliente HTTP para comunicarse con el backend del Proyecto LV.
 */

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const url = `${API_URL}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = `Error ${response.status}`;
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {
      // Sin body JSON
    }
    throw new Error(detail);
  }

  return response.json();
}

export const api = {
  health: () => request("/health"),

  listarVoces: () => request("/api/tts/voices"),

  listarModelos: () => request("/api/tts/models"),

  generarTTS: (payload) =>
    request("/api/tts/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  historial: (limit = 50, createdBy = null) => {
    const params = new URLSearchParams({ limit });
    if (createdBy) params.append("created_by", createdBy);
    return request(`/api/tts/history?${params}`);
  },

  eliminarPrueba: (id) =>
    request(`/api/tts/history/${id}`, { method: "DELETE" }),

  audioUrl: (filename) => `${API_URL}${filename}`,
};