import { useState, useEffect } from "react";

function Health() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/health/")
      .then((response) => response.json())
      .then((data) => {
        setHealthData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <main>
        <h1 className="success">Loading server status...</h1>
      </main>
    );
  }

  if (error) {
    return (
      <main>
        <h1 className="error">Connection Error</h1>
        <p>{error}</p>
      </main>
    );
  }

  return (
    <main>
      <h1 className="success">Server Health Status</h1>

      {healthData && (
        <div className="health-info">
          <p>
            <span className="success">Status:</span> {healthData.status}
          </p>
          <p>
            <span className="success">Environment:</span>{" "}
            {healthData.data?.environment}
          </p>
          {healthData.data?.database && (
            <>
              <p>
                <span className="success">Database:</span>{" "}
                {healthData.data.database.type}
              </p>
              <p>
                <span className="success">DB Status:</span>{" "}
                {healthData.data.database.status}
              </p>
            </>
          )}
        </div>
      )}
    </main>
  );
}

export default Health;
