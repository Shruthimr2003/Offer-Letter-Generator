import React, { useState, type ChangeEvent } from "react";

interface Props {
  label: string; 
  onFileSelect: (file: File) => void;
  loading: boolean;
}

const FileUpload: React.FC<Props> = ({ label, onFileSelect, loading }) => {
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file) return;

    if (!file.name.endsWith(".xlsx")) {
      setError("Only .xlsx files are allowed");
      return;
    }

    setError(null);
    onFileSelect(file);
  };

  return (
    <div className="file-upload">
      <label className="file-label">{label}</label>

      <input
        className="file-input"
        type="file"
        disabled={loading}
        accept=".xlsx"
        onChange={handleChange}
      />

      {error && <p className="status error">{error}</p>}
    </div>
  );
};

export default React.memo(FileUpload);