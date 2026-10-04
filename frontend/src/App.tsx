import { useState } from 'react';
import './App.css';

import Login from './Components/Login';
import GeneralHeader from './Components/GeneralHeader';
import ViajesClientes from './Components/ViajesClientes';
import ViajesStaff from './Components/ViajesStaff';
import ViajesAdmin from './Components/ViajesAdmin';
import GeneralFooter from './Components/GeneralFooter';
import TipoUsuario from './Components/TipoUsuario';

function App() {
  const [login, setLogin] = useState("");
  const [accessToken, setAccessToken] = useState("");

  function handleLogin(accessToken: string) {
    setAccessToken(accessToken);
    setLogin("cargando");
  }

  function handleConnect(rol: string) {
    setLogin(rol);
  }

  return (
    <>
      <GeneralHeader />

      <main>

        {login === "" && (
          <Login onLogin={handleLogin} />
        )}

        {login === "cargando" && (
          <TipoUsuario
            accessToken={accessToken}
            onConnect={handleConnect}
          />
        )}

        {login === "cliente" && (
          <ViajesClientes accessToken={accessToken} />
        )}

        {login === "admin" && (
          <ViajesAdmin accessToken={accessToken} />
        )}

        {login === "staff" && (
          <ViajesStaff accessToken={accessToken} />
        )}

      </main>

      <GeneralFooter />
    </>
  );
}

export default App;