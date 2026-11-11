import { useState } from 'react';
import { Link } from 'react-router';

function RegisterPackagePage() {
  const [pkg, setPkg] = useState(null);

  async function registerPackage(name, destination, weight) {
    const res = await fetch(
      `http://127.0.0.1:8000/packages?name=${name}&destination=${destination}&weight=${weight}&status=pending`,
      { method: "POST" }
    );
    const data = await res.json();
    setPkg(data);
  }

  return (
    <>
      <h2>Register Package</h2>
      <button onClick={() => registerPackage("Electronics Box", "Mumbai", 5.5)}>
        Register Electronics Box (Mumbai)
      </button>
      <button onClick={() => registerPackage("Medical Supplies", "Delhi", 2.0)}>
        Register Medical Supplies (Delhi)
      </button>

      {pkg && (
        <div>
          <h3>Registered Package: {pkg.name}</h3>
          <p>ID: {pkg.id}</p>
          <p>Destination: {pkg.destination}</p>
          <p>Weight: {pkg.weight} kg</p>
          <p>Status: {pkg.status}</p>
          <Link to={`/packages/${pkg.id}`}>View Details</Link>
        </div>
      )}
    </>
  );
}

export default RegisterPackagePage;