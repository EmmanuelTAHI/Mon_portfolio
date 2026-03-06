import { Injectable } from '@angular/core';

/**
 * Translation service to automatically translate French content from backend to English
 * Uses a dictionary mapping approach for common terms and phrases
 */
@Injectable({ providedIn: 'root' })
export class TranslationService {
  private translations: Record<string, string> = {
    // Common words
    'parcours': 'path',
    'certification': 'certification',
    'technique': 'technical',
    'réseaux': 'networks',
    'en cours': 'in progress',
    'en cours d\'obtention': 'in progress',
    'complété': 'completed',
    'complétée': 'completed',
    'obtenu': 'obtained',
    'obtenue': 'obtained',
    'description': 'description',
    'titre': 'title',
    'émetteur': 'issuer',
    'date': 'date',
    
    // Experience related
    'éducation': 'education',
    'formation': 'training',
    'expérience': 'experience',
    'professionnelle': 'professional',
    'personnelle': 'personal',
    
    // Skills related
    'compétence': 'skill',
    'niveau': 'level',
    'catégorie': 'category',
    
    // Projects related
    'projet': 'project',
    'technologies': 'technologies',
    'dépôt': 'repository',
    'démonstration': 'demo',
    'application': 'application',
    'web': 'web',
    'sécurité': 'security',
    'outil': 'tool',
    'script': 'script',
    'automatisation': 'automation',
    
    // Common phrases
    'Parcours de certification technique en réseaux Cisco.': 'Cisco Network Technician Career Path certification.',
    'Certification en cours d\'obtention en penetration testing.': 'Penetration testing certification in progress.',
    'Focused on penetration testing, CTF, and secure development.': 'Focused on penetration testing, CTF, and secure development.',
    'Hands-on practice in offensive security and vulnerability assessment.': 'Hands-on practice in offensive security and vulnerability assessment.',
  };

  /**
   * Translates a string from French to English
   * If no translation is found, returns the original string
   */
  translate(text: string | null | undefined): string {
    if (!text) return '';
    
    const trimmed = text.trim();
    
    // Check for exact match first
    if (this.translations[trimmed]) {
      return this.translations[trimmed];
    }
    
    // Check for case-insensitive match
    const lowerText = trimmed.toLowerCase();
    if (this.translations[lowerText]) {
      return this.translations[lowerText];
    }
    
    // Try to translate common phrases
    for (const [french, english] of Object.entries(this.translations)) {
      if (trimmed.toLowerCase().includes(french.toLowerCase())) {
        return trimmed.replace(new RegExp(french, 'gi'), english);
      }
    }
    
    // If no translation found, return original
    return text;
  }

  /**
   * Translates an object's string properties recursively
   */
  translateObject<T extends Record<string, any>>(obj: T, fields: (keyof T)[]): T {
    const translated = { ...obj };
    
    for (const field of fields) {
      if (typeof translated[field] === 'string') {
        translated[field] = this.translate(translated[field] as string) as T[keyof T];
      }
    }
    
    return translated;
  }

  /**
   * Translates an array of objects
   */
  translateArray<T extends Record<string, any>>(items: T[], fields: (keyof T)[]): T[] {
    return items.map(item => this.translateObject(item, fields));
  }
}
