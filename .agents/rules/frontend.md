# Frontend Guidelines & Conventions

## Tech Stack
- React 18+ / Next.js / TypeScript
- Tailwind CSS with design tokens for agriculture theme (Emerald/Forest/Sage/Slate/Amber)
- Lucide React Icons

## Design System & Tokens
- **Primary Color**: Emerald-600 (`#059669`) / Emerald-500 (`#10b981`)
- **Accent Color**: Lime-500 (`#84cc16`) / Amber-500 (`#f59e0b`)
- **Backgrounds**: Slate-50 / Slate-900 (dark mode)
- **Cards**: Glassmorphism with `bg-white/80 dark:bg-slate-800/80 backdrop-blur-md border border-slate-200/80`
- **Typography**: Inter / Outfit sans-serif

## Component Rules
1. Every component must be written in TypeScript with explicit interfaces/types in `types/`.
2. Do not use inline magic hex codes; use Tailwind utility classes or theme CSS variables.
3. Mobile-first design: large touch targets for camera capture & image upload (minimum 48px tap targets).
4. Disclaimers: Every prediction card and soil metrics display MUST render the non-medical/scientific disclaimer.
5. Error Boundaries & Fallbacks: Always render user-friendly error states, loading skeletons, and empty states.
