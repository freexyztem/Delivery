import { useEffect } from "react";
import { conectarTipoUsuario } from "../Services/api";

interface TipoUsuarioProps {
  accessToken: string;
  onConnect: (rol: string) => void;
}

function TipoUsuario({ accessToken, onConnect }: TipoUsuarioProps) {

  useEffect(() => {
    async function conectar() {
      try {
        const rol = await conectarTipoUsuario(accessToken);
        onConnect(rol);
      } catch (error) {
        console.error("Error conectando usuario:", error);
      }
    }

    conectar();
  }, [accessToken, onConnect]);

  return <p>Cargando usuario...</p>;
}

export default TipoUsuario;