import api from "./api";

export const uploadDocument = async (file: File) => {
  const token = localStorage.getItem("token");

  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/documents/upload", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getDocuments = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/documents", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};
