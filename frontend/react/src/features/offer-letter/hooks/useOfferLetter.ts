import { useState, useCallback } from "react";
import { type OfferLetterState } from "../types/offerLetter.types";

const initialState: OfferLetterState = {
  file: null,
  salaryFile: null,
  docNo: "",
  status: "idle",
  error: null,
  files: [],
};

export const useOfferLetter = () => {
  const [state, setState] = useState<OfferLetterState>(initialState);


  const setFile = useCallback((file: File) => {
    if (!file.name.endsWith(".xlsx")) {
      setState((prev) => ({
        ...prev,
        error: "Only .xlsx files are allowed",
        file: null,
      }));
      return;
    }

    setState((prev) => ({
      ...prev,
      file,
      error: null,
      status: "idle",
      files: [],
    }));
  }, []);


  const setSalaryFile = useCallback((file: File) => {
    if (!file.name.endsWith(".xlsx")) {
      setState((prev) => ({
        ...prev,
        error: "Only .xlsx files are allowed",
        salaryFile: null,
      }));
      return;
    }

    setState((prev) => ({
      ...prev,
      salaryFile: file,
      error: null,
      status: "idle",
    }));
  }, []);

 
  const setDocNo = useCallback((docNo: string) => {
    setState((prev) => ({
      ...prev,
      docNo: docNo.trim(),
    }));
  }, []);


  const generateOfferLetters = useCallback(async () => {
    if (!state.file || !state.salaryFile) {
      setState((prev) => ({
        ...prev,
        error: "Please upload both Excel files",
      }));
      return;
    }

    if (!state.docNo.trim()) {
      setState((prev) => ({
        ...prev,
        error: "Please enter Document Number",
      }));
      return;
    }

    setState((prev) => ({
      ...prev,
      status: "loading",
      error: null,
    }));

    try {
      const formData = new FormData();
      formData.append("file", state.file);
      formData.append("salary_file", state.salaryFile); 
      formData.append("doc_no", state.docNo);

      const uploadRes = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();

      const genRes = await fetch(
        `http://localhost:8000/generate/${uploadData.file_id}`,
        { method: "POST" }
      );

      const data = await genRes.json();

      setState((prev) => ({
        ...prev,
        status: "success",
        files: data.results,
      }));

      return data.results;
    } catch (err: any) {
      setState((prev) => ({
        ...prev,
        status: "error",
        error: err.message || "Something went wrong",
      }));
    }
  }, [state.file, state.salaryFile, state.docNo]);

  return {
    ...state,
    setFile,
    setSalaryFile,
    setDocNo,
    generateOfferLetters,
  };
};