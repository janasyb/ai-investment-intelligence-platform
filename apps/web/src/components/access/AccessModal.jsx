import { useEffect, useRef } from "react";
import AccessForm from "./AccessForm.jsx";

function AccessModal({ open, onClose }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    if (!open) {
      return undefined;
    }

    const previousActiveElement = document.activeElement;

    document.body.classList.add("modal-open");

    requestAnimationFrame(() => {
      dialogRef.current?.focus();
    });

    function handleKeyDown(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.classList.remove("modal-open");

      if (previousActiveElement instanceof HTMLElement) {
        previousActiveElement.focus();
      }
    };
  }, [open, onClose]);

  if (!open) {
    return null;
  }

  return (
    <div
      className="access-modal-backdrop"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) {
          onClose();
        }
      }}
    >
      <div
        ref={dialogRef}
        className="access-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="access-modal-title"
        tabIndex="-1"
      >
        <button
          className="access-modal-close"
          type="button"
          onClick={onClose}
          aria-label="Close early access form"
        >
          ×
        </button>

        <div id="access-modal-title" className="sr-only">
          AIIP Early Access
        </div>

        <AccessForm onSuccess={onClose} />
      </div>
    </div>
  );
}

export default AccessModal;
