export function VoiceSelector({ voces, value, onChange, loading }) {
  return (
    <div className="field">
      <label htmlFor="voice">🎤 Voz</label>
      <select
        id="voice"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading || voces.length === 0}
      >
        <option value="">— Selecciona una voz —</option>
        {voces.map((v) => (
          <option key={v.voice_id} value={v.voice_id}>
            {v.name}
            {v.labels?.gender ? ` (${v.labels.gender})` : ""}
            {v.labels?.accent ? ` · ${v.labels.accent}` : ""}
          </option>
        ))}
      </select>
    </div>
  );
}