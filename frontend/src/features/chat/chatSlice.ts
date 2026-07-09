import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

import type { RootState } from "../../app/store";
import { applyFormPatch } from "../interaction/interactionSlice";

type ChatRole = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: ChatRole;
  content: string;
};

type ChatState = {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
};

const initialState: ChatState = {
  messages: [
    {
      id: "welcome",
      role: "assistant",
      content:
        "Tell me what happened with the HCP, and I will update the interaction form.",
    },
  ],
  isLoading: false,
  error: null,
};

const API_URL = "http://127.0.0.1:8000/api/agent/message";

export const sendChatMessage = createAsyncThunk<
  { assistantMessage: string; formPatch: Record<string, unknown> },
  string,
  { state: RootState }
>("chat/sendChatMessage", async (message, thunkApi) => {
  const state = thunkApi.getState();
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      current_form: state.interaction,
    }),
  });

  if (!response.ok) {
    throw new Error("The AI service returned an error.");
  }

  const data = await response.json();
  thunkApi.dispatch(applyFormPatch(data.form_patch ?? {}));

  return {
    assistantMessage: data.assistant_message,
    formPatch: data.form_patch ?? {},
  };
});

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addUserMessage: (state, action: PayloadAction<string>) => {
      state.messages.push({
        id: crypto.randomUUID(),
        role: "user",
        content: action.payload,
      });
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          content: action.payload.assistantMessage,
        });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message ?? "Something went wrong.";
        state.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "I could not reach the AI service. Check that the FastAPI backend is running.",
        });
      });
  },
});

export const { addUserMessage } = chatSlice.actions;
export default chatSlice.reducer;

