# Component Library
**Framework:** React 18 + TypeScript
**Design System:** Tailwind CSS

## Core Components

### Button
```tsx
import { Button } from '@/components/ui/button'

<Button variant="primary" size="md">
  Click Me
</Button>
```

### Form Input
```tsx
import { Input } from '@/components/ui/input'

<Input 
  type="email" 
  placeholder="Enter email"
  className="w-full"
/>
```

## Usage Guidelines
- All forms must use [[../Forms/Form Standards|Form Standards]]
- Buttons follow [[../Design/Color Palette|Color Palette]]

## Props Documentation
- [[Props/Button Props|Button Props]]
- [[Props/Input Props|Input Props]]