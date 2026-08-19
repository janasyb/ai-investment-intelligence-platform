function Button({
  children,
  href,
  variant = "primary",
  className = "",
  type = "button",
  onClick,
}) {
  const classes = `button button-${variant} ${className}`.trim();

  if (href) {
    return (
      <a href={href} className={classes} onClick={onClick}>
        {children}
      </a>
    );
  }

  return (
    <button type={type} className={classes} onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
