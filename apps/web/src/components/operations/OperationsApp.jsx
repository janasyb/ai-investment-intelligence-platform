import { useEffect, useState } from "react";

import AccessRequestDetail from "./AccessRequestDetail";
import AccessRequestList from "./AccessRequestList";
import "../../styles/operations.css";

const AUTH_LOGIN_PATH = "/api/v1/auth/login";
const AUTH_SESSION_PATH = "/api/v1/auth/session";
const AUTH_LOGOUT_PATH = "/api/v1/auth/logout";

function OperationsApp() {
  const [session, setSession] = useState(null);
  const [state, setState] = useState("loading");
  const [error, setError] = useState("");
  const [selectedRequestId, setSelectedRequestId] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function loadSession() {
      try {
        const response = await fetch(AUTH_SESSION_PATH, {
          credentials: "same-origin",
        });

        if (cancelled) {
          return;
        }

        if (response.ok) {
          const data = await response.json();
          setSession(data);
          setState("authenticated");
          return;
        }

        if (response.status === 401) {
          setState("unauthenticated");
          return;
        }

        if (response.status === 403) {
          setState("forbidden");
          return;
        }

        setError("Unable to verify the operator session.");
        setState("error");
      } catch {
        if (!cancelled) {
          setError("Unable to connect to the AIIP API.");
          setState("error");
        }
      }
    }

    loadSession();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleLogout() {
    try {
      await fetch(AUTH_LOGOUT_PATH, {
        method: "POST",
        credentials: "same-origin",
         headers: {
        "X-CSRF-Token": session?.csrf_token || "",
      },
      });
    } finally {
      window.location.assign("/operations");
    }
  }

  if (state === "loading") {
    return (
      <main className="operations-shell">
        <section className="operations-state">
          <p>Checking operator session...</p>
        </section>
      </main>
    );
  }

  if (state === "unauthenticated") {
    return (
      <main className="operations-shell">
        <section className="operations-state operations-state--auth">
          <p className="operations-eyebrow">AIIP Technologies</p>
          <h1>Operations</h1>
          <p>
            Internal access-request operations require an authorized operator
            session.
          </p>

          <a className="operations-button" href={AUTH_LOGIN_PATH}>
            Sign in
          </a>
        </section>
      </main>
    );
  }

  if (state === "forbidden") {
    return (
      <main className="operations-shell">
        <section className="operations-state operations-state--auth">
          <p className="operations-eyebrow">AIIP Technologies</p>
          <h1>Access denied</h1>
          <p>
            Your authenticated account is not authorized for AIIP operations.
          </p>
        </section>
      </main>
    );
  }

  if (state === "error") {
    return (
      <main className="operations-shell">
        <section className="operations-state operations-state--error">
          <p className="operations-eyebrow">AIIP Technologies</p>
          <h1>Operations unavailable</h1>
          <p>{error}</p>
        </section>
      </main>
    );
  }

  return (
    <main className="operations-shell">
      <header className="operations-header">
        <div>
          <p className="operations-eyebrow">AIIP Technologies</p>
          <h1>Operations</h1>
          <p className="operations-subtitle">
            Early-access request management.
          </p>
        </div>

        <div className="operations-header__actions">
          <div className="operations-operator">
            <span>{session?.name || session?.email || session?.subject}</span>
            <small>{session?.role}</small>
          </div>

          <button
            className="operations-button operations-button--secondary"
            type="button"
            onClick={handleLogout}
          >
            Sign out
          </button>
        </div>
      </header>

      <section className="operations-content">
        {selectedRequestId ? (
          <AccessRequestDetail
            requestId={selectedRequestId}
            csrfToken={session?.csrf_token || ""}
            onBack={() => setSelectedRequestId(null)}
          />
        ) : (
          <AccessRequestList onSelect={setSelectedRequestId} />
        )}
      </section>
    </main>
  );
}

export default OperationsApp;