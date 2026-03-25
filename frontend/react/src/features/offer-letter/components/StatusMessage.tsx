import React from "react";
import { type UploadStatus } from "../types/offerLetter.types";

interface Props {
  status: UploadStatus;
  error: string | null;
}

const StatusMessage: React.FC<Props> = ({ status, error }) => {
  if (status === "loading") {
    return <p className="status loading">Processing... Please wait</p>;
  }

  if (status === "error") {
    return <p className="status error">{error}</p>;
  }

  if (status === "success") {
    return (
      <p className="status success">
        Offer letters generated successfully!
      </p>
    );
  }

  return null;
};

export default React.memo(StatusMessage);