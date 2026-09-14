export function AudioPlayer({ src }) {
  if (!src) return null;

  return (
    <div className="audio-player">
      <audio controls src={src} style={{ width: "100%" }} />
    </div>
  );
}