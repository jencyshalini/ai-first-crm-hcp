import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

import type { RootState } from "../../app/store";

export type InteractionStatus = "Draft" | "Ready to Submit" | "Submitted";

export type InteractionFormState = {
  hcp_name: string;
  specialty: string;
  institution: string;
  interaction_type: string;
  interaction_date: string;
  product_discussed: string;
  discussion_summary: string;
  sentiment: string;
  key_topics: string[];
  materials_shared: string[];
  follow_up_required: boolean;
  follow_up_date: string;
  compliance_flags: string[];
  status: InteractionStatus;
  saved_id: number | null;
  is_saving: boolean;
  save_error: string | null;
};

const initialState: InteractionFormState = {
  hcp_name: "",
  specialty: "",
  institution: "",
  interaction_type: "",
  interaction_date: "",
  product_discussed: "",
  discussion_summary: "",
  sentiment: "",
  key_topics: [],
  materials_shared: [],
  follow_up_required: false,
  follow_up_date: "",
  compliance_flags: [],
  status: "Draft",
  saved_id: null,
  is_saving: false,
  save_error: null,
};

const API_URL = "http://127.0.0.1:8000/api/interactions";

export const saveInteraction = createAsyncThunk<
  { id: number },
  void,
  { state: RootState }
>("interaction/saveInteraction", async (_, thunkApi) => {
  const form = thunkApi.getState().interaction;
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      hcp_name: form.hcp_name,
      specialty: form.specialty,
      institution: form.institution,
      interaction_type: form.interaction_type,
      interaction_date: form.interaction_date,
      product_discussed: form.product_discussed,
      discussion_summary: form.discussion_summary,
      sentiment: form.sentiment,
      key_topics: form.key_topics,
      materials_shared: form.materials_shared,
      follow_up_required: form.follow_up_required,
      follow_up_date: form.follow_up_date,
      compliance_flags: form.compliance_flags,
      status: "Submitted",
    }),
  });

  if (!response.ok) {
    throw new Error("Could not save the interaction.");
  }

  const data = await response.json();
  return { id: data.id };
});

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    applyFormPatch: (state, action: PayloadAction<Partial<InteractionFormState>>) => {
      return {
        ...state,
        ...action.payload,
      };
    },
    resetInteraction: () => initialState,
    markReadyToSubmit: (state) => {
      state.status = "Ready to Submit";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(saveInteraction.pending, (state) => {
        state.is_saving = true;
        state.save_error = null;
      })
      .addCase(saveInteraction.fulfilled, (state, action) => {
        state.is_saving = false;
        state.saved_id = action.payload.id;
        state.status = "Submitted";
      })
      .addCase(saveInteraction.rejected, (state, action) => {
        state.is_saving = false;
        state.save_error = action.error.message ?? "Could not save the interaction.";
      });
  },
});

export const { applyFormPatch, resetInteraction, markReadyToSubmit } =
  interactionSlice.actions;

export default interactionSlice.reducer;
