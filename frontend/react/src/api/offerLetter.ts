const BASE_URL = "http://localhost:8000";

export const uploadExcel = async (file: File,
  salaryFile: File,
  docNo:string
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("salary_file",salaryFile)
  formData.append("doc_no",docNo)

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  return res.json(); 
};

export const generateLetters = async (fileId: string) => {
  const res = await fetch(`${BASE_URL}/generate/${fileId}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Generation failed");
  }

  return res.json(); 
};