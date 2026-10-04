import { useState } from 'react';
import './App.css';
import Login from './Components/Login';
import GeneralHeader from './Components/GeneralHeader';
import ViajesClientes from './Components/ViajesClientes';
import ViajesStaff from './Components/ViajesClientes';
import ViajesAdmin from './Components/ViajesClientes';
import GeneralFooter from './Components/GeneralFooter';

function App() {
  const [login, setLogin] = useState("");
  const [tokens, setTokens] = useState({
    accessToken: null,
    refreshToken: null,
  });

  function handleLogin(accessToken, refreshToken) {
    setTokens({
      accessToken,
      refreshToken,
    });
  }
  
  return (
    <>
      <GeneralHeader/>
      <main>
        {(login === "" ) && <Login onLogin={handleLogin} />}
        {(login === "cliente") && <ViajesClientes/>}
        {(login === "admin") && <ViajesAdmin/>}
        {(login === "staff") && <ViajesStaff/>}
      </main>
      <GeneralFooter/>
    </>
 );
};

export default App;


/*

fetch("http://localhost:8000/api/viajes/", {
  headers: {
    Authorization: `Bearer ${tokens.accessToken}`,
  },
});

*/