export interface Certification {
  id: number;
  title: string;
  issuer: string;
  description: string;
  credential_url: string;
  status: 'completed' | 'in-progress';
  date: string;
  created_at: string;
  updated_at: string;
}
