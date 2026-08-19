import ScoreCard from "./ScoreCard.jsx";

const DIMENSIONS = [
  ["Market", "Analysis"],
  ["Fundamentals", "Analysis"],
  ["Tokenomics", "Analysis"],
  ["Liquidity", "Analysis"],
  ["Risk", "Analysis"],
  ["Evidence", "Synthesis"],
];

function DecisionPanel() {
  return (
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
          <div className="decision-value">
            BUY / HOLD / SELL / WAIT
          </div>
        </div>
      </div>

      <div className="score-grid">
        {DIMENSIONS.map(([label, value]) => (
          <ScoreCard key={label} label={label} value={value} />
        ))}
      </div>

      <div className="panel-footer">
        <span>AIIP Intelligence Engine</span>
        <span>V0.1</span>
      </div>
    </div>
  );
}

export default DecisionPanel;
