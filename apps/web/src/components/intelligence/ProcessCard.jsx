function ProcessCard({ number, title, description }) {
  return (
    <div className="process-card">
      <span>{number}</span>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default ProcessCard;
