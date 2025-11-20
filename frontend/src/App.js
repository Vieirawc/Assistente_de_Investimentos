import React, { useState, useEffect } from 'react'; 
import axios from 'axios'; 
function App() { 
const [projects, setProjects] = useState([]); // Estado para armazenar os projetos 
// useEffect é chamado quando o componente é montado 
useEffect(() => { 
// Fazendo uma requisição GET para o backend na rota /projects 
axios.get('http://localhost:5000/projects') 
.then(response => { 
setProjects(response.data); // Armazena os projetos no 
estado 
}) 
.catch(error => { 
        console.error("Houve um erro ao buscar os projetos!", 
error); 
      }); 
  }, []); // [] garante que o useEffect seja executado apenas uma 
vez 
 
  return ( 
    <div> 
      <h1>Bem-vindo à aplicação de exemplo!</h1> 
      <p>Este é um exemplo de uma Single Page Application (SPA) 
usando React.</p> 
 
      {/* Exibindo os projetos apenas se houver algum */} 
      <h2>Lista de Projetos da ONG</h2> 
      {projects.length === 0 ? ( 
        <p>Nenhum projeto foi adicionado ainda.</p> 
      ) : ( 
        <ul> 
          {projects.map((project, index) => ( 
            <li key={index}> 
              <strong>Nome:</strong> {project.name} <br /> 
              <strong>Descrição:</strong> {project.description} 
            </li> 
          ))} 
        </ul> 
      )} 
    </div> 
  ); 
} 
 
export default App; 