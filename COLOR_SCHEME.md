# Perception Dashboard Color Scheme
**Source:** HustleStats.io

## Color Palette

### Primary Colors
```
Primary Dark:    #18181b (zinc-900) - Logo, buttons, headings
Secondary Dark:  #27272a (zinc-800) - Hover states
Background:      #ffffff (white) - Main background
Card BG:         #f4f4f5 (zinc-50) - Featured sections
```

### Text Colors
```
Heading:         #18181b (zinc-900) - Main headings
Body:            #52525b (zinc-600) - Body text
Muted:           #a1a1aa (zinc-500) - Secondary text
Light Muted:     #d4d4d8 (zinc-300) - Disabled states
Faint:           #71717a (zinc-400) - Hints
```

### UI Elements
```
Border:          #f4f4f5 (zinc-100) - Dividers, borders
Button Border:   #e4e4e7 (zinc-200) - Secondary buttons
Warning BG:      #fef3c7 (amber-50) - Alerts
Warning Text:    #92400e (amber-900) - Alert text
Alert Badge:     #fca5a5 (red-300) - Notification badges
```

## TailwindCSS Configuration

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#18181b',
          dark: '#27272a',
        },
        zinc: {
          50: '#f4f4f5',
          100: '#f4f4f5',
          200: '#e4e4e7',
          300: '#d4d4d8',
          400: '#71717a',
          500: '#a1a1aa',
          600: '#52525b',
          800: '#27272a',
          900: '#18181b',
        },
        warning: {
          bg: '#fef3c7',
          text: '#92400e',
        },
        alert: {
          badge: '#fca5a5',
        }
      }
    }
  }
}
```

## Design Philosophy
- **Minimalist:** Clean, typography-focused design
- **Professional:** Zinc/gray tones, minimal chromatic variation
- **Light Mode Only:** No dark mode (matches HustleStats)
- **Whitespace Priority:** Emphasizes breathing room and clarity
