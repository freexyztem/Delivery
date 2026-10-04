import { useEffect, useState } from "react";
import {
  obtenerEnvios,
  obtenerViajes,
  obtenerProductos,
  type Envio,
  type Viaje,
  type Producto,
} from "../Services/api";
// ============================================================
// PROPS
// ============================================================

interface ViajesClientesProps {
  accessToken: string;
}


// ============================================================
// COMPONENTE
// ============================================================

function ViajesClientes({
  accessToken,
}: ViajesClientesProps) {

  const [envios, setEnvios] = useState<Envio[]>([]);
  const [viajes, setViajes] = useState<Viaje[]>([]);
  const [productos, setProductos] = useState<Producto[]>([]);

  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");


  // ==========================================================
  // CARGAR LOS TRES ENDPOINTS
  // ==========================================================

  useEffect(() => {

    async function cargarDatos() {

      try {

        setCargando(true);
        setError("");

        const [
          enviosData,
          viajesData,
          productosData,
        ] = await Promise.all([
          obtenerEnvios(accessToken),
          obtenerViajes(accessToken),
          obtenerProductos(accessToken),
        ]);

        setEnvios(enviosData);
        setViajes(viajesData);
        setProductos(productosData);

      } catch (error) {

        console.error(error);

        setError(
          "No se pudieron cargar los datos."
        );

      } finally {

        setCargando(false);

      }

    }

    cargarDatos();

  }, [accessToken]);


  // ==========================================================
  // ESTADO DE CARGA
  // ==========================================================

  if (cargando) {
    return (
      <section>
        <p>Cargando tus viajes...</p>
      </section>
    );
  }


  // ==========================================================
  // ESTADO DE ERROR
  // ==========================================================

  if (error) {
    return (
      <section>
        <p>{error}</p>
      </section>
    );
  }


  // ==========================================================
  // AGRUPAR LOS ENVÍOS POR VIAJE
  // ==========================================================

  const enviosPorViaje = envios.reduce(
    (
      grupos: Record<number, Envio[]>,
      envio
    ) => {

      if (!grupos[envio.viaje]) {
        grupos[envio.viaje] = [];
      }

      grupos[envio.viaje].push(envio);

      return grupos;

    },
    {}
  );


  // ==========================================================
  // MOSTRAR VIAJES
  // ==========================================================

  return (
    <section>

      <h1>Mis viajes</h1>

      {Object.entries(enviosPorViaje).map(
        ([viajeId, enviosDelViaje]) => {

          const viaje = viajes.find(
            (viaje) =>
              viaje.id === Number(viajeId)
          );


          // Si por alguna razón el viaje no existe
          // en /viajes/, no mostramos este grupo.

          if (!viaje) {
            return null;
          }


          return (
            <article
              key={viaje.id}
              className="viaje"
            >

              {/* ==========================================
                  INFORMACIÓN DEL VIAJE
              ========================================== */}

              <header>

                <h2>
                  {viaje.nombre}
                </h2>

                <p>
                  Fecha: {viaje.fecha}
                </p>

              </header>


              {/* ==========================================
                  ENVÍOS DEL VIAJE
              ========================================== */}

              <div className="envios">

                {enviosDelViaje.map(
                  (envio) => {

                    const producto =
                      productos.find(
                        (producto) =>
                          producto.id ===
                          envio.producto
                      );


                    if (!producto) {
                      return null;
                    }


                    return (
                      <article
                        key={envio.id}
                        className="producto"
                      >

                        {/* ==========================
                            PRODUCTO
                        ========================== */}

                        <h3>
                          {producto.nombre}
                        </h3>

                        <p>
                          Categoría:{" "}
                          {producto.categoria}
                        </p>


                        {producto.descripcion && (
                          <p>
                            {producto.descripcion}
                          </p>
                        )}


                        {/* ==========================
                            INFORMACIÓN DEL ENVÍO
                        ========================== */}

                        <p>
                          SKU: {envio.sku}
                        </p>

                        <p>
                          Peso: {envio.peso} lb
                        </p>

                        <p>
                          Estado de entrega:{" "}
                          {envio.estado_entrega}
                        </p>

                        <p>
                          Estado de pago:{" "}
                          {envio.estado_pago}
                        </p>

                        <p>
                          Total: $
                          {envio.monto_total}
                        </p>

                        <p>
                          Pagado: $
                          {envio.monto_pagado}
                        </p>

                      </article>
                    );

                  }
                )}

              </div>

            </article>
          );

        }
      )}

    </section>
  );
}

export default ViajesClientes;