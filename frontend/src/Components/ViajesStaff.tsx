interface ViajesStaffProps {
  accessToken: string;
  onRefreshToken?: (
    accessToken: string
  ) => void;
}

export default function ViajesStaff({
  accessToken,
}: ViajesStaffProps) {
  return (
    <section>
      <h2>Viajes Staff</h2>
      <p>AccessToken: {accessToken}</p>
    </section>
  );
}