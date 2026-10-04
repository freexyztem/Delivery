export const API_URL = "https://delivery-r9p0.onrender.com/api/";


// ============================================================
// TIPOS
// ============================================================

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


// ============================================================
// REFRESH ACCESS TOKEN
// ============================================================

export async function refreshAccessToken(): Promise<string> {

  const response = await fetch(`${API_URL}token/refresh/`, {
    method: "POST",

    // Permite enviar la cookie HttpOnly
    credentials: "include",

    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("La sesión ha expirado");
  }

  const data = await response.json();

  return data.access;
}


// ============================================================
// FETCH AUTENTICADO
// ============================================================

export async function fetchWithAuth(
  url: string,
  accessToken: string,
  onRefreshToken: (accessToken: string) => void
): Promise<Response> {

  // ----------------------------------------------------------
  // PRIMER INTENTO
  // ----------------------------------------------------------

  let response = await fetch(url, {
    method: "GET",

    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },

    credentials: "include",
  });


  // ----------------------------------------------------------
  // ACCESS TOKEN TODAVÍA ES VÁLIDO
  // ----------------------------------------------------------

  if (response.status !== 401) {
    return response;
  }


  // ----------------------------------------------------------
  // ACCESS TOKEN EXPIRÓ
  // ----------------------------------------------------------

  console.log("Access token expirado. Intentando renovar...");

  const newAccessToken = await refreshAccessToken();


  // ----------------------------------------------------------
  // GUARDAR EL NUEVO TOKEN EN APP.TSX
  // ----------------------------------------------------------

  onRefreshToken(newAccessToken);


  // ----------------------------------------------------------
  // SEGUNDO INTENTO CON EL NUEVO TOKEN
  // ----------------------------------------------------------

  response = await fetch(url, {
    method: "GET",

    headers: {
      Authorization: `Bearer ${newAccessToken}`,
      "Content-Type": "application/json",
    },

    credentials: "include",
  });

  return response;
}


// ============================================================
// CONECTAR TIPO DE USUARIO
// ============================================================

export async function conectarTipoUsuario(
  accessToken: string,
  onRefreshToken: (accessToken: string) => void
): Promise<string> {

  const response = await fetchWithAuth(
    `${API_URL}usuario/`,
    accessToken,
    onRefreshToken
  );

  if (!response.ok) {
    throw new Error("No se pudo obtener el tipo de usuario");
  }

  const data = await response.json();

  return data.rol;
}


// ============================================================
// OBTENER ENVIOS
// ============================================================

export async function obtenerEnvios(
  accessToken: string,
  onRefreshToken: (accessToken: string) => void
): Promise<Envio[]> {

  const response = await fetchWithAuth(
    `${API_URL}envios/`,
    accessToken,
    onRefreshToken
  );

  if (!response.ok) {
    throw new Error("No se pudieron obtener los envíos");
  }

  return response.json();
}


// ============================================================
// OBTENER VIAJES
// ============================================================

export async function obtenerViajes(
  accessToken: string,
  onRefreshToken: (accessToken: string) => void
): Promise<Viaje[]> {

  const response = await fetchWithAuth(
    `${API_URL}viajes/`,
    accessToken,
    onRefreshToken
  );

  if (!response.ok) {
    throw new Error("No se pudieron obtener los viajes");
  }

  return response.json();
}


// ============================================================
// OBTENER PRODUCTOS
// ============================================================

export async function obtenerProductos(
  accessToken: string,
  onRefreshToken: (accessToken: string) => void
): Promise<Producto[]> {

  const response = await fetchWithAuth(
    `${API_URL}productos/`,
    accessToken,
    onRefreshToken
  );

  if (!response.ok) {
    throw new Error("No se pudieron obtener los productos");
  }

  return response.json();
}