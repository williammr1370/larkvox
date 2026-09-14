import { api } from "../services/api";

export function HistoryTable({ historial, onEliminar, onRefresh }) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>📋 Historial de pruebas</h3>
        <button className="btn btn-secondary btn-sm" onClick={onRefresh}>
          🔄 Refrescar
        </button>
      </div>

      {historial.length === 0 ? (
        <p className="empty">Aún no hay pruebas registradas.</p>
      ) : (
        <div className="table-wrapper">
          <table className="history-table">
            <thead>
              <tr>
                <th>Texto</th>
                <th>Voz</th>
                <th>Modelo</th>
                <th>Latencia</th>
                <th>Autor</th>
                <th>Audio</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {historial.map((p) => (
                <tr key={p.id}>
                  <td className="text-cell" title={p.texto}>
                    {p.texto.length > 40 ? p.texto.slice(0, 40) + "…" : p.texto}
                  </td>
                  <td>{p.voice_name || p.voice_id.slice(0, 8)}</td>
                  <td>
                    <code>{p.model_id.replace("eleven_", "")}</code>
                  </td>
                  <td>
                    <span
                      className={
                        p.latencia_segundos < 0.5
                          ? "badge badge-good"
                          : p.latencia_segundos < 1
                          ? "badge badge-warn"
                          : "badge badge-bad"
                      }
                    >
                      {p.latencia_segundos.toFixed(2)}s
                    </span>
                  </td>
                  <td>{p.created_by || "—"}</td>
                  <td>
                    <audio
                      controls
                      src={api.audioUrl(p.audio_url)}
                      style={{ height: 32, width: 180 }}
                    />
                  </td>
                  <td>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => onEliminar(p.id)}
                      title="Eliminar"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}