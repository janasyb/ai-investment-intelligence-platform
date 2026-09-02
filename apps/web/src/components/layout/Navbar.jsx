function Navbar({ onRequestAccess }) {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <a className="brand" href="/">
          AIIP
        </a>

        <nav className="site-nav" aria-label="Primary navigation">
          <a href="#platform">Platform</a>
          <a href="#intelligence">Intelligence</a>
          <a href="#research">Research</a>
          <a href="#about">About</a>
        </nav>

        <button
          type="button"
          className="button button-primary"
          onClick={onRequestAccess}
        >
          Request Access
        </button>
      </div>
    </header>
  );
}

export default Navbar;
