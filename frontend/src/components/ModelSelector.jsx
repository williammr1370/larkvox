export function ModelSelector({ modelos, value, onChange, loading }) {
  return (
    <div className="field">
      <label htmlFor="model">📦 Modelo</label>
      <select
        id="model"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading}
      >
        {modelos.map((m) => (
          <option key={m.model_id} value={m.model_id}>
            {m.name}
          </option>
        ))}
      </select>
      {modelos.find((m) => m.model_id === value)?.description && (
        <span className="field-hint">
          {modelos.find((m) => m.model_id === value).description}
        </span>
      )}
    </div>
  );
}