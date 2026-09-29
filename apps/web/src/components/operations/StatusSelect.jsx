const STATUS_OPTIONS = [
  "pending",
  "reviewed",
  "contacted",
  "interview",
  "qualified",
  "report",
  "paid",
  "converted",
  "rejected",
];

function StatusSelect({ value, onChange, disabled = false }) {
  return (
    <label className="operations-status-control">
      <span>Status</span>

      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
      >
        {STATUS_OPTIONS.map((status) => (
          <option key={status} value={status}>
            {status}
          </option>
        ))}
      </select>
    </label>
  );
}

export { STATUS_OPTIONS };
export default StatusSelect;