function IntelligenceList({ items }) {
  return (
    <div className="intelligence-list">
      {items.map((item, index) => (
        <div key={item} >
          <span>{String(index + 1).padStart(2, "0")}</span>
          <strong>{item}</strong>
        </div>
      ))}
    </div>
  );
}

export default IntelligenceList;
