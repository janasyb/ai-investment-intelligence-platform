import { useEffect, useState } from "react";

const ACCESS_REQUESTS_PATH = "/api/v1/operations/access-requests";

function AccessRequestList({ onSelect }) {
  const [requests, setRequests] = useState([]);
  const [state, setState] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadRequests() {
      try {
        const response = await fetch(ACCESS_REQUESTS_PATH, {
          credentials: "same-origin",
        });

        if (cancelled) {
          return;
        }

        if (response.ok) {
          const data = await response.json();
          setRequests(data);
          setState("ready");
          return;
        }

        if (response.status === 401) {
          window.location.assign("/operations");
          return;
        }

        if (response.status === 403) {
          setError("You are not authorized to view access requests.");
          setState("error");
          return;
        }

        setError("Unable to load access requests.");
        setState("error");
      } catch {
        if (!cancelled) {
          setError("Unable to connect to the AIIP API.");
          setState("error");
        }
      }
    }

    loadRequests();

    return () => {
      cancelled = true;
    };
  }, []);

  if (state === "loading") {
    return (
      <section className="operations-panel">
        <p className="operations-eyebrow">Early Access</p>
        <h2>Access requests</h2>
        <p className="operations-muted">Loading requests...</p>
      </section>
    );
  }

  if (state === "error") {
    return (
      <section className="operations-panel operations-panel--error">
        <p className="operations-eyebrow">Early Access</p>
        <h2>Access requests</h2>
        <p className="operations-error">{error}</p>
      </section>
    );
  }

  if (requests.length === 0) {
    return (
      <section className="operations-panel">
        <p className="operations-eyebrow">Early Access</p>
        <h2>Access requests</h2>
        <p className="operations-muted">
          No early-access requests have been submitted yet.
        </p>
      </section>
    );
  }

  return (
    <section className="operations-panel">
      <div className="operations-panel__heading">
        <div>
          <p className="operations-eyebrow">Early Access</p>
          <h2>Access requests</h2>
        </div>

        <span className="operations-count">
          {requests.length} request{requests.length === 1 ? "" : "s"}
        </span>
      </div>

      <div className="operations-table-wrapper">
        <table className="operations-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Profile</th>
              <th>Status</th>
              <th>Submitted</th>
              <th />
            </tr>
          </thead>

          <tbody>
            {requests.map((request) => (
              <tr key={request.id}>
                <td>{request.name}</td>
                <td>{request.email}</td>
                <td>{request.profile}</td>
                <td>
                  <span className="operations-status">
                    {request.status}
                  </span>
                </td>
                <td>
                  {new Date(request.created_at).toLocaleDateString()}
                </td>
                <td>
                  <button
                    className="operations-link-button"
                    type="button"
                    onClick={() => onSelect(request.id)}
                  >
                    Open
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default AccessRequestList;