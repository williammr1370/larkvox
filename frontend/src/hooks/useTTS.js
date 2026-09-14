import { useState, useCallback } from "react";
import { api } from "../services/api";

/**
 * Hook para gestionar la generación de TTS.
 */
export function useTTS() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resultado, setResultado] = useState(null);

  const generar = useCallback(async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.generarTTS(payload);
      setResultado(data);
      return data;
    } catch (e) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  const limpiar = useCallback(() => {
    setResultado(null);
    setError(null);
  }, []);

  return { generar, loading, error, resultado, limpiar };
}