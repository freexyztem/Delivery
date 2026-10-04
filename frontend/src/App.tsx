import { useState } from "react";
//import "./App.css";

import Login from "./Components/Login";
import GeneralHeader from "./Components/GeneralHeader";
import ViajesClientes from "./Components/ViajesClientes";
import ViajesStaff from "./Components/ViajesStaff";
import ViajesAdmin from "./Components/ViajesAdmin";
import GeneralFooter from "./Components/GeneralFooter";
import TipoUsuario from "./Components/TipoUsuario";


function App() {

  const [login, setLogin] = useState("");
  const [accessToken, setAccessToken] = useState("");


  // ==========================================================
  // LOGIN
  // ==========================================================

  function handleLogin(accessToken: string) {

    setAccessToken(accessToken);

    setLogin("cargando");
  }


  // ==========================================================
  // TIPO DE USUARIO
  // ==========================================================

  function handleConnect(rol: string) {

    setLogin(rol);
  }


  return (
    <>

      <GeneralHeader />

      <main>

        {/* ==================================================
            LOGIN
        ================================================== */}

        {login === "" && (
          <Login onLogin={handleLogin} />
        )}


        {/* ==================================================
            CONECTANDO USUARIO
        ================================================== */}

        {login === "cargando" && (
          <TipoUsuario
            accessToken={accessToken}
            onConnect={handleConnect}
            onRefreshToken={setAccessToken}
          />
        )}


        {/* ==================================================
            CLIENTE
        ================================================== */}

        {login === "cliente" && (
          <ViajesClientes
            accessToken={accessToken}
            onRefreshToken={setAccessToken}
          />
        )}


        {/* ==================================================
            ADMIN
        ================================================== */}

        {login === "admin" && (
          <ViajesAdmin
            accessToken={accessToken}
            onRefreshToken={setAccessToken}
          />
        )}


        {/* ==================================================
            STAFF
        ================================================== */}

        {login === "staff" && (
          <ViajesStaff
            accessToken={accessToken}
            onRefreshToken={setAccessToken}
          />
        )}

      </main>

      <GeneralFooter />

    </>
  );
}


export default App;