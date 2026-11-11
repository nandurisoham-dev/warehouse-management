import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router'

function PackageDetailPage() {
  const { id } = useParams();
  const [pkg, setPkg] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadPackage() {
      const res = await fetch(`http://127.0.0.1:8000/packages/${id}`);
      if (res.ok) {
        const data = await res.json();
        setPkg(data);
      } else {
        setMessage("Package not found");
      }
    }
    loadPackage();
  }, [id]);

  async function updateStatus() {
    const res = await fetch(
      `http://127.0.0.1:8000/packages/${id}?status=dispatched`,
      { method: "PATCH" }
    );
    if (res.ok) {
      const data = await res.json();
      setPkg(data);
      setMessage("Status updated to dispatched");
    }
  }

  async function deletePackage() {
    const res = await fetch(`http://127.0.0.1:8000/packages/${id}`, {
      method: "DELETE"
    });
    const data = await res.json();
    if (res.ok) {
      setPkg(null);
      setMessage("Package deleted");
    } else {
      setMessage(data.detail);
    }
  }

  if (!pkg) return (
    <>
      <Link to="/">← Back to register</Link>
      <p>{message || "Loading ....."}</p>
    </>
  );

  return (
    <>
      <Link to="/">← Back to register</Link>
      <h2>{pkg.name}</h2>
      <p>ID: {pkg.id}</p>
      <p>Destination: {pkg.destination}</p>
      <p>Weight: {pkg.weight} kg</p>
      <p>Arrival Date: {pkg.arrival_date}</p>
      <p>Status: {pkg.status}</p>

      <button onClick={updateStatus}>Mark as Dispatched</button>
      <button onClick={deletePackage}>Delete Package</button>

      {message && <p>{message}</p>}
    </>
  );
}

export default PackageDetailPage;