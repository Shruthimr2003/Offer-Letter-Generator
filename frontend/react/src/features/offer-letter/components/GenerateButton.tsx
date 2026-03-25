import React from "react";

interface Props {
  onGenerate: () => void;
  loading: boolean;
  disabled?: boolean;
}

const GenerateButton: React.FC<Props> = ({
  onGenerate,
  loading,
  disabled,
}) => {
  return (
    <button
      className="button"
      onClick={onGenerate}
      disabled={loading || disabled}
    >
      {loading ? "Generating..." : "Generate Offer Letters"}
    </button>
  );
};

export default React.memo(GenerateButton);