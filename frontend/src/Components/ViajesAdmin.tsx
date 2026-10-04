interface ViajesAdminProps {
  accessToken: string;
  onRefreshToken?: (
    accessToken: string
  ) => void;
}

export default function ViajesAdmin({
  accessToken,
}: ViajesAdminProps) {
  return (
    <section>
      <h2>Viajes Admin</h2>
      <p>AccessToken: {accessToken}</p>
    </section>
  );
}