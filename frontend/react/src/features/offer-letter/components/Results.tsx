import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { type GeneratedFile } from "../types/offerLetter.types";

const Results: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const files = (location.state as { files: GeneratedFile[] })?.files || [];

    if (!files.length) {
        return (
            <div className="full-container">
                <p>No results found.</p>
                <button className="button" onClick={() => navigate("/")}>
                    Go Back
                </button>
            </div>
        );
    }

    return (
        <div className="full-container">
            <div className="results-header">
                <button className="back-arrow" onClick={() => navigate("/")}>
                    ←
                </button>
                <h2>Generated Offer Letters</h2>
            </div>

            <div className="scroll-area">
                {files.map((file, index) => (
                    <div key={index} className="results-item">
                        <span>{file.candidate}</span>
                        <a
                            className="download-btn"
                            href={`http://localhost:8000/download/${file.filename}`}
                            download
                        >
                            Download
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Results;