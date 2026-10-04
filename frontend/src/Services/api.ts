export const API_URL = "https://delivery-r9p0.onrender.com/api/token/";

export default async function obtenerViajesClientes(accessToken) {
  const response = await fetch(
    "http://localhost:8000/api/viajes/",
    {
      headers: {
        Authorization: `Bearer ${tokens.accessToken}`,
      },
    }
  );

  if (response.status === 401) {
    const nuevoAccessToken = await refreshAccessToken();

    const retry = await fetch(
      "http://localhost:8000/api/viajes/",
      {
        headers: {
          Authorization: `Bearer ${nuevoAccessToken}`,
        },
      }
    );

    return retry.json();
  }

  return response.json();
}