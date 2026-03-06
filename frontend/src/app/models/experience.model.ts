export interface Experience {
  id: number;
  title: string;
  organization: string;
  experience_type: string;
  location: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string;
  order: number;
  created_at: string;
}
