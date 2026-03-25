import React from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../features/offer-letter/components/FileUpload";
import GenerateButton from "../features/offer-letter/components/GenerateButton";
import StatusMessage from "../features/offer-letter/components/StatusMessage";
import { useOfferLetter } from "../features/offer-letter/hooks/useOfferLetter";

const Home: React.FC = () => {
  const {
    file,
    salaryFile,
    docNo,
    status,
    setFile,
    error,
    setSalaryFile,
    setDocNo,
    generateOfferLetters,
  } = useOfferLetter();

  const navigate = useNavigate();
  const isLoading = status === "loading";

  const handleGenerate = async () => {
    const result = await generateOfferLetters();

    if (result?.length) {
      navigate("/results", { state: { files: result } });
    }
  };

  return (
    <div className="container">
      <h2 className="title">Offer Letter Generator</h2>

      <div className="section">
        <div className="section">
          <FileUpload
            label="Candidate Details"
            onFileSelect={setFile}
            loading={isLoading}
          />
        </div>
      </div>

      <div className="section">
        <FileUpload label="Salary details" onFileSelect={setSalaryFile} loading={isLoading} />
      </div>

      <div className="section">
        <h4>Document Number</h4>
        <input
          type="text"
          value={docNo}
          onChange={(e) => setDocNo(e.target.value)}
          placeholder="e.g. DOC010"
          className="text-input"
        />
      </div>

      <div className="section">
        <GenerateButton
          onGenerate={handleGenerate}
          loading={isLoading}
          disabled={!file || !salaryFile || !docNo}
        />
      </div>

      <div className="section">
        <StatusMessage status={status} error={error} />
      </div>
    </div>
  );
};

export default Home;
