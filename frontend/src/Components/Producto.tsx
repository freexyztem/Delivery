interface ProductoProps {
  producto: string;
  precio: number;
  peso: number;
  unidad: string;
  moneda: string;
  cambio: number;
}

export default function Producto({ producto, precio, peso, unidad, moneda, cambio }: ProductoProps) {
  return (
    <div className="producto">
      <p><strong>Producto:</strong> {producto}</p>
      <p><strong>Precio:</strong> {(moneda ==="USD")? precio.toFixed(2): (precio * cambio).toFixed(2)} {moneda} </p>
      <p><strong>Peso:</strong> { (unidad === "lb")? peso.toFixed(2): (peso/2.20462).toFixed(2)} {unidad}</p>
    </div>
  );
}