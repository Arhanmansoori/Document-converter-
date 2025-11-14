import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const uploadFile = async (file, endpoint) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE}${endpoint}`, formData, {
    responseType: "blob", // we want a binary file
  });

  // Create a temporary blob URL for download
  const blob = new Blob([response.data], { type: "application/pdf" });
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = downloadUrl;
  a.download = file.name.replace(/\.[^/.]+$/, ".pdf"); // change extension to .pdf
  document.body.appendChild(a);
  a.click();
  a.remove();

  // Optional: get latest conversion metadata
  try {
    const info = await axios.get(`${API_BASE}/conversion/latest`);
    return info.data;
  } catch (err) {
    console.error("Could not fetch conversion info:", err);
    return null;
  }
};
