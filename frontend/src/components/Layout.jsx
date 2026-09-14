import { USUARIOS } from "../constants/presets";

export function Layout({ children, usuario, setUsuario }) {
  return (
    <div className="layout">
      <header className="layout-header">
        <div className="layout-title">
          <span className="logo">🎙️</span>
          <div>
            <h1>Proyecto LarkVox</h1>
            <p className="subtitle">Panel de Pruebas TTS · v0.1</p>
          </div>
        </div>

        <div className="layout-user">
          <label htmlFor="usuario">Usuario:</label>
          <select
            id="usuario"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
          >
            {USUARIOS.map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
        </div>
      </header>

      <main className="layout-main">{children}</main>

      <footer className="layout-footer">
        Proyecto LV · Call Center con IA · {new Date().getFullYear()}
      </footer>
    </div>
  );
}