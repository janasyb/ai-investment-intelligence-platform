function Navbar({ onRequestAccess }) {
  return (
    <header className="navbar">
      <div className="brand">
        <div className="brand-mark">A</div>

        <div>
          <div className="brand-name">AIIP</div>
          <div className="brand-subtitle">
            AI Investment Intelligence
          </div>
        </div>
      </div>

      <nav className="nav-links" aria-label="Primary navigation">
        <a href="#platform">Platform</a>
        <a href="#intelligence">Intelligence</a>
        <a href="#research">Research</a>
        <a href="#about">About</a>
      </nav>

      <button
        type="button"
        className="nav-button"
        onClick={onRequestAccess}
      >
        Request Access
      </button>
    </header>
  );
}

export default Navbar;
