interface ViajesAdminProps {
  accessToken: string;
}

export default function ViajesAdmin({ accessToken }: ViajesAdminProps) {
  return (
    <section>
      <h2>Viajes Admin</h2>
      <p>AccessToken: {accessToken}</p>
    </section>
  );
}