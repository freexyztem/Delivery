export const API_URL = "https://delivery-r9p0.onrender.com/api/";

interface obtenerViajesClientesProps {
  accessToken: string;
}

export default async function obtenerViajesClientes({ accessToken }: obtenerViajesClientesProps) {
  const response = await fetch(
    `${API_URL}viajes/`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (response.status === 401) {
    const nuevoAccessToken = await refreshAccessToken();

    const retry = await fetch(
      `${API_URL}token/refresh/`,
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

function refreshAccessToken() {
  // Implementation for refreshing access token
}