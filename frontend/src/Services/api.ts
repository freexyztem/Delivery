export const API_URL = "https://delivery-r9p0.onrender.com/api/";


// Paso 2 - Conectar tipo de usuario
export async function conectarTipoUsuario(accessToken: string): Promise<string> {
  const response = await fetch(`${API_URL}usuario/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("No se pudo obtener el tipo de usuario");
  }

  const data = await response.json();

  return data.rol;
}

// FASE 3 - Pedir Productos de Viajes (envios, productos y viajes)
export interface Envio {
  id: number;
  viaje: number;
  producto: number;
  cliente: number;
  sku: string;
  qr_token: string;
  peso: string;
  tarifa: number;
  gastos_empresa: string;
  extra_fee: string;
  precio_fijo: string;
  estado_entrega: string;
  estado_pago: string;
  monto_total: string;
  monto_pagado: string;
  creado_en: string;
  actualizado_en: string;
}
export interface Viaje {
  id: number;
  nombre: string;
  fecha: string;
  creado_en: string;
}
export interface Producto {
  id: number;
  nombre: string;
  cliente: number;
  descripcion: string;
  categoria: string;
  creado_en: string;
}
//------------ENVIOS
export async function obtenerEnvios(
  accessToken: string
): Promise<Envio[]> {

  const response = await fetch(`${API_URL}envios/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("No se pudieron obtener los envíos");
  }

  return response.json();
}
//------------VIAJES
export async function obtenerViajes(
  accessToken: string
): Promise<Viaje[]> {

  const response = await fetch(`${API_URL}viajes/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("No se pudieron obtener los viajes");
  }

  return response.json();
}
//------------PRODUCTOS
export async function obtenerProductos(
  accessToken: string
): Promise<Producto[]> {

  const response = await fetch(`${API_URL}productos/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("No se pudieron obtener los productos");
  }

  return response.json();
}

function refreshAccessToken() {
  // Implementation for refreshing access token
}

