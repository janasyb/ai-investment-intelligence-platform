import { useEffect, useRef, useState } from "react";
import Button from "../common/Button.jsx";

function Navbar({ activeSection = "", onNavigate }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuButtonRef = useRef(null);

  const links = [
    { id: "platform", label: "Platform" },
    { id: "intelligence", label: "Intelligence" },
    { id: "research", label: "Research" },
    { id: "about", label: "About" },
  ];

  useEffect(() => {
    if (!menuOpen) {
      return undefined;
    }

    const handleEscape = (event) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
        menuButtonRef.current?.focus();
      }
    };

    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("keydown", handleEscape);
    };
  }, [menuOpen]);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";

    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const handleNavigate = (event, id) => {
    setMenuOpen(false);

    if (onNavigate) {
      onNavigate(event, id);
    }
  };

  return (
    <header className="navbar">
      <a href="#" className="brand" aria-label="AIIP home">
        <div className="brand-mark">A</div>

        <div>
          <div className="brand-name">AIIP</div>
          <div className="brand-subtitle">
            AI Investment Intelligence
          </div>
        </div>
      </a>

      <nav className="nav-links" aria-label="Primary navigation">
        {links.map((link) => (
          <a
            key={link.id}
            href={`#${link.id}`}
            className={activeSection === link.id ? "active" : ""}
            aria-current={activeSection === link.id ? "page" : undefined}
            onClick={(event) => handleNavigate(event, link.id)}
          >
            {link.label}
          </a>
        ))}
      </nav>

      <div className="navbar-actions">
        <Button href="#access" className="nav-button">
          Request Access
        </Button>

        <button
          ref={menuButtonRef}
          type="button"
          className={`menu-toggle ${menuOpen ? "is-open" : ""}`}
          aria-label={menuOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={menuOpen}
          aria-controls="mobile-navigation"
          onClick={() => setMenuOpen((current) => !current)}
        >
          <span />
          <span />
          <span />
        </button>
      </div>

      <div
        id="mobile-navigation"
        className={`mobile-navigation ${menuOpen ? "is-open" : ""}`}
        aria-hidden={!menuOpen}
      >
        <nav aria-label="Mobile navigation">
          {links.map((link) => (
            <a
              key={link.id}
              href={`#${link.id}`}
              className={activeSection === link.id ? "active" : ""}
              onClick={(event) => handleNavigate(event, link.id)}
              tabIndex={menuOpen ? 0 : -1}
            >
              <span>{link.label}</span>
              <span aria-hidden="true">→</span>
            </a>
          ))}

          <a
            href="#access"
            className="mobile-access-link"
            onClick={() => setMenuOpen(false)}
            tabIndex={menuOpen ? 0 : -1}
          >
            Request Early Access
          </a>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
