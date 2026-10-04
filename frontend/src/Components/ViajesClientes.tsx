import Producto from "./Producto";
import obtenerViajesClientes from '../Services/api';

interface ViajesClientesProps {
  accessToken: string;
}

export default function ViajesClientes({ accessToken }: ViajesClientesProps) {
  const moneda = "USD";
  const cambio = 1.2;
  const datos = async () => {
    const viajes = await obtenerViajesClientes(accessToken);
    // Procesar los datos de los viajes
  };

  datos();
  return (
    <section>
      <h2><span className="material-symbols-outlined">travel</span><br />20-julio-2027</h2>
      <Producto producto={"Zapatos"} precio={100} peso={2} unidad={"lb"} moneda={moneda} cambio={cambio} />
      <Producto producto={"Camiseta"} precio={20} peso={0.5} unidad={"kg"} moneda={moneda} cambio={cambio} />
      <Producto producto={"Pantalones"} precio={50} peso={1} unidad={"kg"} moneda={moneda} cambio={cambio} />
    </section>
  );
}