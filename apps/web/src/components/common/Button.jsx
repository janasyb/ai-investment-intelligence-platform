function Button({
  children,
  href,
  variant = "primary",
  className = "",
  type = "button",
  onClick,
  ariaLabel,
}) {
  const classes = `button button-${variant} ${className}`.trim();

  if (href) {
    return (
      <a
        href={href}
        className={classes}
        onClick={onClick}
        aria-label={ariaLabel}
      >
        {children}
      </a>
    );
  }

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      aria-label={ariaLabel}
    >
      {children}
    </button>
  );
}

export default Button;
