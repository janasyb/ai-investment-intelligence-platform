import { useEffect, useState } from "react";

import StatusSelect from "./StatusSelect";

const ACCESS_REQUEST_PATH = "/api/v1/operations/access-requests";

function AccessRequestDetail({ requestId, csrfToken, onBack }) {
  const [request, setRequest] = useState(null);
  const [state, setState] = useState("loading");
  const [error, setError] = useState("");
  const [statusState, setStatusState] = useState("idle");
  const [statusError, setStatusError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadRequest() {
      try {
        const response = await fetch(
          `${ACCESS_REQUEST_PATH}/${requestId}`,
          {
            credentials: "same-origin",
          }
        );

        if (cancelled) {
          return;
        }

        if (response.ok) {
          const data = await response.json();
          setRequest(data);
          setState("ready");
          return;
        }

        if (response.status === 401) {
          window.location.assign("/operations");
          return;
        }

        if (response.status === 403) {
          setError("You are not authorized to view this request.");
          setState("error");
          return;
        }

        if (response.status === 404) {
          setError("The access request could not be found.");
          setState("error");
          return;
        }

        setError("Unable to load the access request.");
        setState("error");
      } catch {
        if (!cancelled) {
          setError("Unable to connect to the AIIP API.");
          setState("error");
        }
      }
    }

    loadRequest();

    return () => {
      cancelled = true;
    };
  }, [requestId]);

  async function handleStatusChange(nextStatus) {
    if (!request || nextStatus === request.status) {
      return;
    }

    setStatusState("saving");
    setStatusError("");

    try {
      const response = await fetch(
        `${ACCESS_REQUEST_PATH}/${requestId}/status`,
        {
          method: "PATCH",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-Token": csrfToken,
          },
          body: JSON.stringify({
            status: nextStatus,
          }),
        }
      );

      if (response.ok) {
        const updatedRequest = await response.json();
        setRequest(updatedRequest);
        setStatusState("saved");
        return;
      }

      if (response.status === 401) {
        window.location.assign("/operations");
        return;
      }

      if (response.status === 403) {
        setStatusError(
          "You are not authorized to update this request."
        );
        setStatusState("error");
        return;
      }

      if (response.status === 404) {
        setStatusError("The access request could not be found.");
        setStatusState("error");
        return;
      }

      setStatusError("Unable to update the request status.");
      setStatusState("error");
    } catch {
      setStatusError("Unable to connect to the AIIP API.");
      setStatusState("error");
    }
  }

  if (state === "loading") {
    return (
      <section className="operations-panel">
        <button
          className="operations-link-button"
          type="button"
          onClick={onBack}
        >
          ← Back to requests
        </button>

        <p className="operations-eyebrow">Early Access</p>
        <h2>Request details</h2>
        <p className="operations-muted">Loading request...</p>
      </section>
    );
  }

  if (state === "error") {
    return (
      <section className="operations-panel operations-panel--error">
        <button
          className="operations-link-button"
          type="button"
          onClick={onBack}
        >
          ← Back to requests
        </button>

        <p className="operations-eyebrow">Early Access</p>
        <h2>Request details</h2>
        <p className="operations-error">{error}</p>
      </section>
    );
  }

  return (
    <section className="operations-panel operations-detail">
      <button
        className="operations-link-button"
        type="button"
        onClick={onBack}
      >
        ← Back to requests
      </button>

      <div className="operations-panel__heading">
        <div>
          <p className="operations-eyebrow">Early Access</p>
          <h2>Request details</h2>
        </div>

        <span className="operations-status">{request.status}</span>
      </div>

      <div className="operations-detail-grid">
        <div className="operations-detail-field">
          <span>Name</span>
          <strong>{request.name}</strong>
        </div>

        <div className="operations-detail-field">
          <span>Email</span>
          <strong>{request.email}</strong>
        </div>

        <div className="operations-detail-field">
          <span>Profile</span>
          <strong>{request.profile}</strong>
        </div>

        <div className="operations-detail-field">
          <span>Consent</span>
          <strong>{request.consent ? "Granted" : "Not granted"}</strong>
        </div>

        <div className="operations-detail-field">
          <span>Submitted</span>
          <strong>
            {new Date(request.created_at).toLocaleString()}
          </strong>
        </div>

        <div className="operations-detail-field">
          <span>Last updated</span>
          <strong>
            {new Date(request.updated_at).toLocaleString()}
          </strong>
        </div>
      </div>

      <div className="operations-detail-section">
        <p className="operations-eyebrow">Customer challenge</p>
        <p className="operations-detail-challenge">
          {request.challenge}
        </p>
      </div>

      <div className="operations-detail-section operations-status-section">
        <StatusSelect
          value={request.status}
          onChange={handleStatusChange}
          disabled={statusState === "saving"}
        />

        {statusState === "saving" && (
          <p className="operations-muted">Saving status...</p>
        )}

        {statusState === "saved" && (
          <p className="operations-success">Status updated.</p>
        )}

        {statusState === "error" && (
          <p className="operations-error">{statusError}</p>
        )}
      </div>
    </section>
  );
}

export default AccessRequestDetail;