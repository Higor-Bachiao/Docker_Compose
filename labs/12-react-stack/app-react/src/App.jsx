import { useState } from "react";

const PRATICAS = ["Containers", "Dockerfile", "Volumes", "Redes", "Compose", "Multi-stage"];

export default function App() {
  const [feitas, setFeitas] = useState([]);

  const alternar = (nome) =>
    setFeitas((atual) =>
      atual.includes(nome) ? atual.filter((n) => n !== nome) : [...atual, nome]
    );

  return (
    <main className="container">
      <h1>SD 2026B — hot reload funcionando!</h1>
      <p>
        Código editado no host, Vite observando dentro do container: salvar
        <code> src/App.jsx</code> atualiza esta página sem rebuild.
      </p>
      <div className="chips">
        {PRATICAS.map((p) => (
          <button key={p} className={feitas.includes(p) ? "ok" : ""} onClick={() => alternar(p)}>
            {feitas.includes(p) ? "✔ " : ""}{p}
          </button>
        ))}
      </div>
      <p className="placar">{feitas.length} de {PRATICAS.length} tópicos revisados</p>
    </main>
  );
}
