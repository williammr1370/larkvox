import { useState, useEffect, useCallback } from "react";
import { Layout } from "./components/Layout";
import { TTSForm } from "./components/TTSForm";
import { ResultCard } from "./components/ResultCard";
import { HistoryTable } from "./components/HistoryTable";
import { useTTS } from "./hooks/useTTS";
import { api } from "./services/api";
import { MODELOS_DISPONIBLES } from "./constants/presets";

function App() {
  const [usuario, setUsuario] = useState(
    localStorage.getItem("lv_usuario") || "William"
  );
  const [voces, setVoces] = useState([]);
  const [modelos, setModelos] = useState(MODELOS_DISPONIBLES);
  const [historial, setHistorial] = useState([]);
  const [cargandoInicial, setCargandoInicial] = useState(true);

  const { generar, loading, error, resultado, limpiar } = useTTS();

  useEffect(() => {
    localStorage.setItem("lv_usuario", usuario);
  }, [usuario]);

  useEffect(() => {
    async function cargar() {
      try {
        const [v, m, h] = await Promise.all([
          api.listarVoces().catch(() => []),
          api.listarModelos().catch(() => []),
          api.historial(30).catch(() => []),
        ]);

        setVoces(v);

        if (m.length > 0) {
          const idsInteresantes = MODELOS_DISPONIBLES.map((x) => x.model_id);
          const filtrados = m.filter((x) =>
            idsInteresantes.includes(x.model_id)
          );
          setModelos(filtrados.length > 0 ? filtrados : MODELOS_DISPONIBLES);
        }

        setHistorial(h);
      } catch (e) {
        console.error("Error cargando datos iniciales:", e);
      } finally {
        setCargandoInicial(false);
      }
    }
    cargar();
  }, []);

  const refrescarHistorial = useCallback(async () => {
    try {
      const h = await api.historial(30);
      setHistorial(h);
    } catch (e) {
      console.error(e);
    }
  }, []);

  const handleSubmit = async (payload) => {
    try {
      await generar({ ...payload, created_by: usuario });
      await refrescarHistorial();
    } catch (e) {
      // El error ya está manejado en el hook
    }
  };

  const handleEliminar = async (id) => {
    if (!confirm("¿Eliminar esta prueba?")) return;
    try {
      await api.eliminarPrueba(id);
      await refrescarHistorial();
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  return (
    <Layout usuario={usuario} setUsuario={setUsuario}>
      {cargandoInicial ? (
        <div className="loading">Cargando configuración...</div>
      ) : (
        <div className="container">
          <TTSForm
            voces={voces}
            modelos={modelos}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />

          {resultado && <ResultCard resultado={resultado} onLimpiar={limpiar} />}

          <HistoryTable
            historial={historial}
            onEliminar={handleEliminar}
            onRefresh={refrescarHistorial}
          />
        </div>
      )}
    </Layout>
  );
}

export default App;