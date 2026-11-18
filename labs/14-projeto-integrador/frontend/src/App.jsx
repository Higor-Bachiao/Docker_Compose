import { useEffect, useState } from "react";

const VAZIO = { nome: "", ra: "", periodo: 8 };

export default function App() {
  const [alunos, setAlunos] = useState(null);
  const [erro, setErro] = useState(null);
  const [form, setForm] = useState(VAZIO);
  const [aviso, setAviso] = useState("");

  const carregar = () =>
    fetch("/api/alunos")
      .then((r) => r.json())
      .then(setAlunos)
      .catch((e) => setErro(String(e)));

  useEffect(() => {
    carregar();
  }, []);

  async function cadastrar(evento) {
    evento.preventDefault();
    const r = await fetch("/api/alunos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, periodo: Number(form.periodo) }),
    });
    const corpo = await r.json();
    setAviso(r.ok ? `${corpo.nome} cadastrado(a).` : `Erro: ${corpo.erro}`);
    if (r.ok) setForm(VAZIO);
    carregar();
  }

  // DESAFIO P14: botão de exclusão -> DELETE /api/alunos/:id -> Nginx -> backend -> Postgres
  async function excluir(aluno) {
    const r = await fetch(`/api/alunos/${aluno.id}`, { method: "DELETE" });
    setAviso(r.ok ? `${aluno.nome} removido(a).` : "Não foi possível remover.");
    carregar();
  }

  return (
    <main className="container">
      <h1>Projeto Integrador — SD 2026B</h1>
      <p className="sub">React (Nginx) → API Node → PostgreSQL, cada um no seu container.</p>

      <form onSubmit={cadastrar}>
        <input placeholder="Nome" value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} required />
        <input placeholder="RA" value={form.ra} onChange={(e) => setForm({ ...form, ra: e.target.value })} required />
        <input type="number" min="1" max="10" value={form.periodo} onChange={(e) => setForm({ ...form, periodo: e.target.value })} />
        <button type="submit">Cadastrar</button>
      </form>
      {aviso && <p className="aviso">{aviso}</p>}

      {erro && <p className="erro">Erro ao consultar a API: {erro}</p>}
      {!erro && !alunos && <p>Carregando alunos...</p>}

      {alunos && (
        <table>
          <thead>
            <tr><th>ID</th><th>RA</th><th>Nome</th><th>Período</th><th></th></tr>
          </thead>
          <tbody>
            {alunos.map((a) => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.ra}</td>
                <td>{a.nome}</td>
                <td>{a.periodo}º</td>
                <td><button className="excluir" onClick={() => excluir(a)}>Excluir</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {alunos && <p className="sub">{alunos.length} aluno(s) no banco.</p>}
    </main>
  );
}
