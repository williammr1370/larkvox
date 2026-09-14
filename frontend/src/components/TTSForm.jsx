import { useState } from "react";
import { TEXT_PRESETS } from "../constants/presets";
import { VoiceSelector } from "./VoiceSelector";
import { ModelSelector } from "./ModelSelector";

export function TTSForm({ voces, modelos, onSubmit, loading, error }) {
  const [texto, setTexto] = useState(TEXT_PRESETS[0].text);
  const [voiceId, setVoiceId] = useState("");
  const [modelId, setModelId] = useState(
    modelos[0]?.model_id || "eleven_flash_v2_5"
  );
  const [stability, setStability] = useState(0.5);
  const [similarity, setSimilarity] = useState(0.75);
  const [avanzado, setAvanzado] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!voiceId) {
      alert("Selecciona una voz primero");
      return;
    }
    onSubmit({
      texto,
      voice_id: voiceId,
      voice_name: voces.find((v) => v.voice_id === voiceId)?.name || null,
      model_id: modelId,
      stability,
      similarity_boost: similarity,
    });
  };

  const aplicarPreset = (preset) => {
    setTexto(preset.text);
  };

  return (
    <form className="card tts-form" onSubmit={handleSubmit}>
      <h2>🧪 Nueva prueba</h2>

      <div className="field">
        <label htmlFor="texto">📝 Texto a convertir</label>
        <textarea
          id="texto"
          rows={4}
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          maxLength={5000}
          placeholder="Escribe el texto que quieres convertir a voz..."
        />
        <div className="presets">
          <span className="presets-label">Presets:</span>
          {TEXT_PRESETS.map((p) => (
            <button
              key={p.id}
              type="button"
              className="chip"
              onClick={() => aplicarPreset(p)}
            >
              {p.label}
            </button>
          ))}
        </div>
        <div className="char-count">{texto.length}/5000 caracteres</div>
      </div>

      <div className="grid-2">
        <VoiceSelector
          voces={voces}
          value={voiceId}
          onChange={setVoiceId}
          loading={loading}
        />
        <ModelSelector
          modelos={modelos}
          value={modelId}
          onChange={setModelId}
          loading={loading}
        />
      </div>

      <button
        type="button"
        className="btn btn-link"
        onClick={() => setAvanzado(!avanzado)}
      >
        {avanzado ? "▼" : "▶"} Configuración avanzada
      </button>

      {avanzado && (
        <div className="grid-2 advanced">
          <div className="field">
            <label>
              Stability: <code>{stability.toFixed(2)}</code>
            </label>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={stability}
              onChange={(e) => setStability(parseFloat(e.target.value))}
            />
          </div>
          <div className="field">
            <label>
              Similarity boost: <code>{similarity.toFixed(2)}</code>
            </label>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={similarity}
              onChange={(e) => setSimilarity(parseFloat(e.target.value))}
            />
          </div>
        </div>
      )}

      {error && <div className="alert alert-error">❌ {error}</div>}

      <div className="actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !voiceId || !texto.trim()}
        >
          {loading ? "⏳ Generando..." : "🔊 Generar y probar"}
        </button>
      </div>
    </form>
  );
}