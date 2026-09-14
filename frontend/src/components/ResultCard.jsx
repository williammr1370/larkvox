import { AudioPlayer } from "./AudioPlayer";
import { api } from "../services/api";

export function ResultCard({ resultado }) {
  if (!resultado) return null;

  return (
    <div className="card result-card">
      <h3>📊 Último resultado</h3>

      <div className="result-metrics">
        <div className="metric">
          <span className="metric-label">⏱️ Latencia</span>
          <span className="metric-value">
            {resultado.latencia_segundos.toFixed(2)} s
          </span>
        </div>
        <div className="metric">
          <span className="metric-label">📁 Tamaño</span>
          <span className="metric-value">
            {resultado.tamaño_kb.toFixed(1)} KB
          </span>
        </div>
        <div className="metric">
          <span className="metric-label">📦 Modelo</span>
          <span className="metric-value">
            {resultado.model_id.replace("eleven_", "")}
          </span>
        </div>
        <div className="metric">
          <span className="metric-label">🎤 Voz</span>
          <span className="metric-value">
            {resultado.voice_name || resultado.voice_id.slice(0, 8)}
          </span>
        </div>
      </div>

      <AudioPlayer src={api.audioUrl(resultado.audio_url)} />
    </div>
  );
}