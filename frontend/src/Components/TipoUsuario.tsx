import { useEffect } from "react";

import {
  conectarTipoUsuario,
} from "../Services/api";


interface TipoUsuarioProps {

  accessToken: string;

  onConnect: (rol: string) => void;

  onRefreshToken: (
    accessToken: string
  ) => void;
}


export default function TipoUsuario({
  accessToken,
  onConnect,
  onRefreshToken,
}: TipoUsuarioProps) {


  useEffect(() => {

    async function conectar() {

      try {

        const rol = await conectarTipoUsuario(
          accessToken,
          onRefreshToken
        );

        onConnect(rol);

      } catch (error) {

        console.error(
          "Error obteniendo tipo de usuario:",
          error
        );

      }
    }


    if (accessToken) {
      conectar();
    }

  }, [
    accessToken,
    onConnect,
    onRefreshToken,
  ]);


  return (
    <section>

      <p>
        Cargando información del usuario...
      </p>

    </section>
  );
}