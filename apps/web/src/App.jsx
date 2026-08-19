import "./styles/index.css";
import Navbar from "./components/layout/Navbar.jsx";
import Footer from "./components/layout/Footer.jsx";

function App() {
  return (
    <div className="site-shell">
      <Navbar />

      <main>
        <section className="hero">
          <div className="hero-content">
            <div className="eyebrow">
              INVESTMENT INTELLIGENCE FOR DIGITAL ASSETS
            </div>

            <h1>
              Make better digital-asset
              <span> investment decisions.</span>
            </h1>

            <p className="hero-description">
              AIIP structures fragmented market, fundamental, tokenomic,
              liquidity, and risk information into decision intelligence
              designed to help investors evaluate opportunities with greater
              clarity.
            </p>

            <div className="hero-actions">
              <a href="#platform" className="button button-primary">
                Explore AIIP
              </a>

              <a href="#research" className="button button-secondary">
                View Research
              </a>
            </div>

            <div className="hero-note">
              Built for evidence-driven digital-asset research.
            </div>
          </div>

          <div className="decision-panel">
            <div className="panel-header">
              <div>
                <div className="panel-label">AIIP DECISION INTELLIGENCE</div>
                <div className="asset-name">Digital Asset Analysis</div>
              </div>

              <div className="status-badge">RESEARCH</div>
            </div>

            <div className="asset-summary">
              <div>
                <div className="metric-label">Decision Framework</div>
                <div className="decision-value">BUY / HOLD / SELL / WAIT</div>
              </div>
            </div>

            <div className="score-grid">
              <div className="score-card">
                <span>Market</span>
                <strong>Analysis</strong>
              </div>

              <div className="score-card">
                <span>Fundamentals</span>
                <strong>Analysis</strong>
              </div>

              <div className="score-card">
                <span>Tokenomics</span>
                <strong>Analysis</strong>
              </div>

              <div className="score-card">
                <span>Liquidity</span>
                <strong>Analysis</strong>
              </div>

              <div className="score-card">
                <span>Risk</span>
                <strong>Analysis</strong>
              </div>

              <div className="score-card">
                <span>Evidence</span>
                <strong>Synthesis</strong>
              </div>
            </div>

            <div className="panel-footer">
              <span>AIIP Intelligence Engine</span>
              <span>V0.1</span>
            </div>
          </div>
        </section>

        <section className="trust-strip">
          <div>STRUCTURED RESEARCH</div>
          <div>EVIDENCE SYNTHESIS</div>
          <div>DECISION INTELLIGENCE</div>
          <div>RISK AWARENESS</div>
        </section>

        <section id="platform" className="section">
          <div className="section-heading">
            <div className="section-number">01</div>

            <div>
              <div className="eyebrow">THE PROBLEM</div>

              <h2>
                Digital-asset research is
                <span> fragmented.</span>
              </h2>

              <p>
                Investors increasingly have access to more information than
                ever before. The challenge is determining what matters,
                understanding conflicting evidence, and translating research
                into a structured decision process.
              </p>
            </div>
          </div>

          <div className="problem-grid">
            <article>
              <div className="card-number">01</div>
              <h3>Too much information</h3>
              <p>
                Market data, news, social signals, tokenomics, on-chain
                activity, and research are distributed across many sources.
              </p>
            </article>

            <article>
              <div className="card-number">02</div>
              <h3>Conflicting evidence</h3>
              <p>
                Different sources can tell different stories about the same
                asset, making independent evaluation difficult.
              </p>
            </article>

            <article>
              <div className="card-number">03</div>
              <h3>Decision uncertainty</h3>
              <p>
                The difficult part is often not finding information. It is
                understanding what the evidence means for the decision.
              </p>
            </article>
          </div>
        </section>

        <section id="intelligence" className="section dark-section">
          <div className="center-heading">
            <div className="eyebrow">AIIP INTELLIGENCE</div>

            <h2>
              From information
              <span> to intelligence.</span>
            </h2>

            <p>
              AIIP is designed to synthesize relevant evidence into a
              structured investment-research workflow.
            </p>
          </div>

          <div className="process-grid">
            <div className="process-card">
              <span>01</span>
              <h3>Discover</h3>
              <p>
                Identify relevant market, asset, and investment information.
              </p>
            </div>

            <div className="process-card">
              <span>02</span>
              <h3>Analyze</h3>
              <p>
                Examine market, fundamental, tokenomic, liquidity, and risk
                factors.
              </p>
            </div>

            <div className="process-card">
              <span>03</span>
              <h3>Synthesize</h3>
              <p>
                Bring relevant evidence together into a structured research
                view.
              </p>
            </div>

            <div className="process-card">
              <span>04</span>
              <h3>Decide</h3>
              <p>
                Support a disciplined evaluation of BUY, HOLD, SELL, or WAIT
                decisions.
              </p>
            </div>
          </div>
        </section>

        <section id="research" className="section">
          <div className="research-layout">
            <div>
              <div className="eyebrow">DECISION INTELLIGENCE</div>

              <h2>
                A structured view of
                <span> investment evidence.</span>
              </h2>

              <p>
                AIIP research is designed to help investors examine multiple
                dimensions of a digital asset rather than relying on a single
                metric, headline, or market narrative.
              </p>

              <a href="#access" className="text-link">
                Explore the research framework â†’
              </a>
            </div>

            <div className="intelligence-list">
              <div>
                <span>01</span>
                <strong>Market Intelligence</strong>
              </div>

              <div>
                <span>02</span>
                <strong>Fundamental Analysis</strong>
              </div>

              <div>
                <span>03</span>
                <strong>Tokenomics</strong>
              </div>

              <div>
                <span>04</span>
                <strong>Liquidity & Execution</strong>
              </div>

              <div>
                <span>05</span>
                <strong>Risk Intelligence</strong>
              </div>

              <div>
                <span>06</span>
                <strong>Evidence Synthesis</strong>
              </div>
            </div>
          </div>
        </section>

        <section id="access" className="access-section">
          <div className="access-content">
            <div className="eyebrow">AIIP V0.1</div>

            <h2>
              Research the decision.
              <span> Not the noise.</span>
            </h2>

            <p>
              AIIP is being developed as an investment-intelligence platform
              for people who want a more structured way to evaluate digital
              assets.
            </p>

            <button className="button button-primary">
              Request Early Access
            </button>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default App;
