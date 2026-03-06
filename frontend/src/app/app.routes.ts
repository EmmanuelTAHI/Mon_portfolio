import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'project/:slug',
    loadComponent: () =>
      import('./features/project-detail/project-detail.component').then(
        (m) => m.ProjectDetailComponent
      ),
  },
  {
    path: '_my_challenge',
    loadComponent: () =>
      import('./features/challenge/challenge.component').then(
        (m) => m.ChallengeComponent
      ),
  },
  {
    path: '_my_challenge/image',
    loadComponent: () =>
      import('./features/challenge/image-viewer/image-viewer.component').then(
        (m) => m.ImageViewerComponent
      ),
  },
  { path: '**', redirectTo: '' },
];
