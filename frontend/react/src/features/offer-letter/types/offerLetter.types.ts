export type UploadStatus = "idle" | "loading" | "success" | "error";

export interface GeneratedFile {
  candidate: string;
  filename: string;
}

export interface OfferLetterState {
  file: File | null;
  docNo:string
  salaryFile :File | null,
  status: UploadStatus;
  error: string | null;
  files: GeneratedFile[];
}