import { useAppDispatch, useAppSelector } from "../app/hooks";
import { saveInteraction } from "../features/interaction/interactionSlice";

function Field({
  label,
  value,
  wide = false,
}: {
  label: string;
  value: string;
  wide?: boolean;
}) {
  return (
    <label className={wide ? "field field-wide" : "field"}>
      <span>{label}</span>
      <input value={value || "-"} disabled />
    </label>
  );
}

function TextAreaField({ label, value }: { label: string; value: string }) {
  return (
    <label className="field field-wide">
      <span>{label}</span>
      <textarea value={value || "-"} disabled />
    </label>
  );
}

export function InteractionForm() {
  const dispatch = useAppDispatch();
  const form = useAppSelector((state) => state.interaction);
  const canSave = Boolean(form.hcp_name && form.discussion_summary);

  return (
    <section className="panel form-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Interaction Details</p>
          <h1>Log HCP Interaction</h1>
        </div>
        <span className="status-pill">{form.status}</span>
      </div>

      <div className="notice">
        This form is AI-controlled. Use the assistant to add or edit details.
      </div>

      <div className="form-grid">
        <Field label="HCP Name" value={form.hcp_name} />
        <Field label="Specialty" value={form.specialty} />
        <Field label="Institution / Account" value={form.institution} />
        <Field label="Interaction Type" value={form.interaction_type} />
        <Field label="Interaction Date" value={form.interaction_date} />
        <Field label="Product Discussed" value={form.product_discussed} />
        <Field label="Sentiment" value={form.sentiment} />
        <Field
          label="Follow-up Required"
          value={form.follow_up_required ? "Yes" : "No"}
        />
        <Field label="Follow-up Date" value={form.follow_up_date} />
        <Field
          label="Key Topics"
          value={form.key_topics.length ? form.key_topics.join(", ") : ""}
          wide
        />
        <Field
          label="Materials Shared"
          value={
            form.materials_shared.length ? form.materials_shared.join(", ") : ""
          }
          wide
        />
        <TextAreaField
          label="Discussion Summary"
          value={form.discussion_summary}
        />
        <Field
          label="Compliance Flags"
          value={
            form.compliance_flags.length
              ? form.compliance_flags.join(", ")
              : "No flags"
          }
          wide
        />
      </div>

      <div className="form-actions">
        {form.saved_id ? (
          <span className="saved-note">Saved interaction #{form.saved_id}</span>
        ) : (
          <span className="saved-note">Review AI-filled details before saving.</span>
        )}
        <button
          type="button"
          onClick={() => dispatch(saveInteraction())}
          disabled={!canSave || form.is_saving}
        >
          {form.is_saving ? "Saving..." : "Save Interaction"}
        </button>
      </div>

      {form.save_error ? (
        <div className="form-error">{form.save_error}</div>
      ) : null}
    </section>
  );
}
