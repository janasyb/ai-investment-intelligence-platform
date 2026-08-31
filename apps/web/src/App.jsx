import { useState } from "react";
import "./styles/index.css";

import Button from "./components/common/Button.jsx";
import Navbar from "./components/layout/Navbar.jsx";
import Footer from "./components/layout/Footer.jsx";
import DecisionPanel from "./components/intelligence/DecisionPanel.jsx";
import ProcessCard from "./components/intelligence/ProcessCard.jsx";
import IntelligenceList from "./components/intelligence/IntelligenceList.jsx";
import useActiveSection from "./hooks/useActiveSection.js";
import AccessModal from "./components/access/AccessModal.jsx";

const SECTION_IDS = [
  "platform",
  "intelligence",
  "research",
  "about",
];

const PROCESS_STEPS = [
  {
    number: "01",
    title: "Discover",
    description:
      "Identify relevant market, asset, and investment information.",
  },
  {
    number: "02",
    title: "Analyze",
    description:
      "Examine market, fundamental, tokenomic, liquidity, and risk factors.",
  },
  {
    number: "03",
    title: "Synthesize",
    description:
      "Bring relevant evidence together into a structured research view.",
  },
  {
    number: "04",
    title: "Decide",
    description:
      "Support a disciplined evaluation of BUY, HOLD, SELL, or WAIT decisions.",
  },
];

const INTELLIGENCE_ITEMS = [
  "Market Intelligence",
  "Fundamental Analysis",
  "Tokenomics",
  "Liquidity & Execution",
  "Risk Intelligence",
  "Evidence Synthesis",
];

function App() {
  const activeSection = useActiveSection(SECTION_IDS);

  const [accessOpen, setAccessOpen] = useState(false);

  const handleNavigate = (event, id) => {
    const target = document.getElementById(id);

    if (!target) {
      return;
    }

    event.preventDefault();

    target.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });

    window.history.replaceState(null, "", `#${id}`);
  };

  return (
    <div className="site-shell">
      <Navbar
        activeSection={activeSection}
        onNavigate={handleNavigate}
      />

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
              designed to help investors evaluate opportunities with
              greater clarity.
            </p>

            <div className="hero-actions">
              <Button href="#platform">
                Explore AIIP
              </Button>

              <Button href="#research" variant="secondary">
                View Research
              </Button>
            </div>

            <div className="hero-note">
              Built for evidence-driven digital-asset research.
            </div>
          </div>

          <DecisionPanel />
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
                understanding conflicting evidence, and translating
                research into a structured decision process.
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
            {PROCESS_STEPS.map((step) => (
              <ProcessCard
                key={step.number}
                number={step.number}
                title={step.title}
                description={step.description}
              />
            ))}
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
                dimensions of a digital asset rather than relying on a
                single metric, headline, or market narrative.
              </p>

              <Button href="#access" variant="secondary" className="text-link">
                Explore the research framework →
              </Button>
            </div>

            <IntelligenceList items={INTELLIGENCE_ITEMS} />
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

            <Button href="#access">
              Request Early Access
            </Button>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default App;
