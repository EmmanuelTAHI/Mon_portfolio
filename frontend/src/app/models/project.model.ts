export interface Project {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  description: string;
  category: string;
  technologies: string;
  github_url?: string;
  repo_url?: string; // Pour compatibilité avec l'ancien format
  demo_url: string | null;
  image: string | null;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}
