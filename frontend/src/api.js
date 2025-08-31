const API_URL = "http://localhost:5000"; // depois mudamos para o service do docker-compose

export async function getUsuarios() {
  const res = await fetch(`${API_URL}/usuarios`);
  return res.json();
}

export async function addUsuario(usuario) {
  const res = await fetch(`${API_URL}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario),
  });
  return res.json();
}
