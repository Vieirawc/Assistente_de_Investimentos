import { useState, useEffect } from "react";
import { getUsuarios, addUsuario } from "./api";


function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [nome, setNome] = useState("");
  const [salario, setSalario] = useState("");

  useEffect(() => {
    carregarUsuarios();
  }, []);

  async function carregarUsuarios() {
    const data = await getUsuarios();
    setUsuarios(data);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    await addUsuario({ nome, salario });
    setNome("");
    setSalario("");
    carregarUsuarios();
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Assistente de Investimentos</h1>
      <p> Cadastro de Usuário: </p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
        <input
          type="number"
          placeholder="Salário"
          value={salario}
          onChange={(e) => setSalario(e.target.value)}
        />
        <button type="submit">Cadastrar</button>
      </form>

      <h2>Usuários</h2>
      <ul>
        {usuarios.map((u, i) => (
          <li key={i}>
            {u.nome} - R$ {u.salario}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
