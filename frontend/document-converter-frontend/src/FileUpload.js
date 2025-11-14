import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [conversionType, setConversionType] = useState("/convert/word-to-pdf");
  const [message, setMessage] = useState("");
  const [meta, setMeta] = useState(null);

  const handleSubmit = async (e) => {
  e.preventDefault();
  if (!file) {
    setMessage("Please select a file first.");
    return;
  }

  setMessage("⏳ Converting, please wait...");

  try {
    const formData = new FormData();
    formData.append("file", file);

    const backendUrl = "http://127.0.0.1:8000" + conversionType;

    // Important: Tell Axios we expect binary data
    const response = await axios.post(backendUrl, formData, {
      responseType: "blob",
      headers: { "Content-Type": "multipart/form-data" },
    });

    // ✅ Force browser to download the file
    const blob = new Blob([response.data], { type: "application/pdf" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    // Choose correct filename extension
    const ext = conversionType.includes("pdf") ? ".pdf" : "";
    a.download = file.name.replace(/\.[^/.]+$/, ext);
    document.body.appendChild(a);
    a.click();
    a.remove();

    // ✅ Optional: fetch latest metadata
    const info = await axios.get("http://127.0.0.1:8000/conversion/latest");
    setMeta(info.data);
    setMessage("✅ Conversion successful! File downloaded.");
  } catch (error) {
    console.error("Error during conversion:", error);
    setMessage("❌ Conversion failed. Check console for details.");
  }
};


  return (
    <div style={{ textAlign: "center", marginTop: "40px" }}>
      <h2>📄 Document Converter</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".docx,.html,.pdf,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginBottom: "10px" }}
        />
        <br />
        <select
          value={conversionType}
          onChange={(e) => setConversionType(e.target.value)}
          style={{ padding: "8px", marginBottom: "10px" }}
        >
          <option value="/convert/word-to-pdf">Word → PDF</option>
          <option value="/convert/html-to-pdf">HTML → PDF</option>
          <option value="/convert/pdf-to-image-pdf">PDF → Image-PDF</option>
          <option value="/convert/excel-to-pdf">Excel → PDF</option>
        </select>
        <br />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            background: "#007bff",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Convert & Download
        </button>
      </form>

      <p style={{ marginTop: "20px" }}>{message}</p>

      {meta && (
        <div
          style={{
            marginTop: "20px",
            display: "inline-block",
            textAlign: "left",
            background: "#f7f7f7",
            padding: "15px",
            borderRadius: "10px",
          }}
        >
          <h4>Latest Conversion Info:</h4>
          <p><strong>Filename:</strong> {meta.original_filename}</p>
          <p><strong>Type:</strong> {meta.conversion_type}</p>
          <p><strong>Converted Path:</strong> {meta.converted_path}</p>
          <p><strong>Timestamp:</strong> {new Date(meta.timestamp).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
