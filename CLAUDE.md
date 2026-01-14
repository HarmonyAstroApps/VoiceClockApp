# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website for "Talking Clock Pro" - a mobile app that provides time announcements. The site is built with vanilla HTML, CSS, and JavaScript, featuring a bilingual interface (English/Japanese) and smooth animations.

## Architecture

### Core Structure
- **index.html**: Main landing page with all sections (hero, features, benefits, contact, privacy)
- **src/styles/globals.css**: All CSS styles using CSS custom properties for theming
- **src/scripts/**: JavaScript modules for functionality
  - `translations.js`: Bilingual content management and language switching
  - `screenshot-scroll.js`: Interactive screenshot carousel with smooth scrolling

### Design System
The site uses CSS custom properties defined in `:root`:
- `--primary-color: #4A90E2` (blue)
- `--secondary-color: #8E44AD` (purple) 
- `--accent-color: #E74C3C` (red)
- `--spacing-unit: 8px` (base spacing multiplier)

### Internationalization
- Content is managed through the `translations` object in `translations.js`
- Language switching preserves user preference in localStorage
- All translatable content uses `data-i18n` attributes
- Currently supports English (en) and Japanese (ja)

## Key Features

### Screenshot Carousel
- Smooth auto-scrolling with pause on hover/interaction
- Touch/drag support for mobile devices
- Infinite loop animation using duplicated image sets
- Located in `.screenshot-showcase` section

### Responsive Design
- Mobile-first approach with touch-friendly interactions
- Fixed navigation with backdrop blur effect
- Smooth scrolling and CSS animations throughout

## Development Commands

This is a static website with no build process. To work with it:

**Local Development:**
- Serve files using any static file server
- Example: `python -m http.server 8000` or `npx serve .`

**Deployment:**
- The site is hosted on GitHub Pages
- Main URL: https://avinashkr29.github.io/TalkingClockPro/
- Files are served directly from the repository

## File Organization

```
/
├── index.html              # Main page with all content
├── public/images/          # Static assets
│   ├── content/           # App screenshots and demo content
│   └── logos/             # Brand assets
├── src/
│   ├── scripts/           # JavaScript functionality
│   └── styles/            # CSS styling
└── app-ads.txt           # Google AdSense verification
```

## Making Changes

### Adding New Content Sections
1. Add HTML structure to `index.html`
2. Add corresponding styles to `src/styles/globals.css`
3. If translatable, add entries to both `en` and `ja` objects in `translations.js`
4. Use `data-i18n` attributes for translatable text

### Styling Guidelines
- Use CSS custom properties for consistent theming
- Follow the `var(--spacing-unit)` system for spacing
- Maintain the existing color scheme and design patterns
- Ensure responsive behavior across all screen sizes

### Adding New Languages
1. Extend the `translations` object in `translations.js`
2. Update the language toggle logic to support additional languages
3. Test all content sections for proper translation coverage

### Developer rules
1. confirm me with the changes that you are going to proceed with. tell me your plan before you proceed and verfiy the changes at the end.always think about the user experience, the ui, /ux, the flow, and make is awesome/wow feel.
2. Ask me for more guidelines if you are confused of need more details.
3. always check that there are no compiling error, and that the app will run once you are done. if error, correct it. 
4. Very important: While coding, desigining, or anything, think like an apple designer. Keep it minimalistic, clean, premium, aesthetics, and macos like.
5. **Commit Guidelines**: Keep commit messages short and concise (1-2 lines max). NEVER include Claude/AI authorship credits or "Generated with Claude Code" in commits. Write commits as if done by the human developer.
