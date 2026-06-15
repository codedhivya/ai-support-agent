import api from "./api";

export const createSession = async () => {
  const token = localStorage.getItem("token");

  const response = await api.post(
    "/chat/session",
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );

  return response.data;
};

export const askQuestion = async (sessionId: string, question: string) => {
  const token = localStorage.getItem("token");

  const response = await api.post(
    "/chat/ask",
    {
      session_id: sessionId,
      question,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );

  return response.data;
};
