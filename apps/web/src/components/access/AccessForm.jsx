import { useState } from "react";

const INITIAL_FORM = {
  name: "",
  email: "",
  profile: "",
  challenge: "",
  consent: false,
};

function AccessForm() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState("idle");

  function updateField(event) {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));

    setErrors((current) => ({
      ...current,
      [name]: "",
    }));
  }

  function validate() {
    const nextErrors = {};

    if (!form.name.trim()) {
      nextErrors.name = "Name is required.";
    }

    if (!form.email.trim()) {
      nextErrors.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      nextErrors.email = "Enter a valid email address.";
    }

    if (!form.profile) {
      nextErrors.profile = "Select the option that best describes you.";
    }

    if (!form.challenge.trim()) {
      nextErrors.challenge = "Tell us what you want AIIP to help you research.";
    }

    if (!form.consent) {
      nextErrors.consent = "Consent is required to submit your request.";
    }

    return nextErrors;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const nextErrors = validate();

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    setStatus("submitting");

    try {
      const response = await fetch("/api/v1/access-requests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name.trim(),
          email: form.email.trim(),
          profile: form.profile,
          challenge: form.challenge.trim(),
          consent: form.consent,
        }),
      });

      if (!response.ok) {
        throw new Error("Access request could not be submitted.");
      }

      setStatus("success");
      setForm(INITIAL_FORM);
      setErrors({});

    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="access-success" role="status">
        <div className="access-success-mark">✓</div>

        <h3>Request received.</h3>

        <p>
          Thank you for your interest in AIIP. We will review your request
          and follow up with early-access information.
        </p>
      </div>
    );
  }

  return (
    <form className="access-form" onSubmit={handleSubmit} noValidate>
      <div className="access-form-heading">
        <div className="eyebrow">AIIP EARLY ACCESS</div>

        <h3>Request access to AIIP.</h3>

        <p>
          Tell us a little about how you research digital assets so we can
          understand where AIIP can create the most value.
        </p>
      </div>

      <div className="form-field">
        <label htmlFor="access-name">Name</label>

        <input
          id="access-name"
          name="name"
          type="text"
          value={form.name}
          onChange={updateField}
          autoComplete="name"
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? "access-name-error" : undefined}
        />

        {errors.name && (
          <span id="access-name-error" className="form-error">
            {errors.name}
          </span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="access-email">Email</label>

        <input
          id="access-email"
          name="email"
          type="email"
          value={form.email}
          onChange={updateField}
          autoComplete="email"
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email ? "access-email-error" : undefined}
        />

        {errors.email && (
          <span id="access-email-error" className="form-error">
            {errors.email}
          </span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="access-profile">I am primarily a...</label>

        <select
          id="access-profile"
          name="profile"
          value={form.profile}
          onChange={updateField}
          aria-invalid={Boolean(errors.profile)}
          aria-describedby={
            errors.profile ? "access-profile-error" : undefined
          }
        >
          <option value="">Select one</option>
          <option value="individual-investor">Individual investor</option>
          <option value="researcher">Researcher / analyst</option>
          <option value="trader">Trader</option>
          <option value="advisor">Investment advisor</option>
          <option value="fund-professional">Fund / investment professional</option>
          <option value="other">Other</option>
        </select>

        {errors.profile && (
          <span id="access-profile-error" className="form-error">
            {errors.profile}
          </span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="access-challenge">
          What is your biggest digital-asset research challenge?
        </label>

        <textarea
          id="access-challenge"
          name="challenge"
          value={form.challenge}
          onChange={updateField}
          rows="4"
          aria-invalid={Boolean(errors.challenge)}
          aria-describedby={
            errors.challenge ? "access-challenge-error" : undefined
          }
        />

        {errors.challenge && (
          <span id="access-challenge-error" className="form-error">
            {errors.challenge}
          </span>
        )}
      </div>

      <div className="form-consent">
        <label>
          <input
            name="consent"
            type="checkbox"
            checked={form.consent}
            onChange={updateField}
          />

          <span>
            I agree to be contacted about AIIP early access and product
            research.
          </span>
        </label>

        {errors.consent && (
          <span className="form-error">{errors.consent}</span>
        )}
      </div>

      {status === "error" && (
        <div className="form-submit-error" role="alert">
          We could not submit your request right now. Please try again.
        </div>
      )}

      <button
        className="button button-primary access-submit"
        type="submit"
        disabled={status === "submitting"}
      >
        {status === "submitting" ? "Submitting..." : "Request Early Access"}
      </button>

      <p className="access-privacy-note">
        Never submit passwords, private keys, seed phrases, or financial
        account credentials.
      </p>
    </form>
  );
}

export default AccessForm;
