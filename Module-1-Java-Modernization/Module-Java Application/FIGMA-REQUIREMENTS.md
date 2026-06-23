# Figma Design Requirements - BTN Bank Ticketing System

## 📋 Project Overview

**Application Name:** Bank Customer Service Ticketing System  
**Purpose:** Modernize the UI/UX of a legacy Java 8 banking ticketing application  
**Target Users:** Bank customer service agents, supervisors, and administrators  
**Design Goal:** Transform legacy 90s-style interface into modern, professional banking application

---

## 🎯 Design Objectives

### Primary Goals
1. **Modernization**: Replace outdated Windows 95-style UI with contemporary design
2. **Professionalism**: Reflect bank's corporate identity and trustworthiness
3. **Efficiency**: Streamline ticket management workflow for agents
4. **Accessibility**: Ensure WCAG 2.1 AA compliance for all users
5. **Responsiveness**: Support desktop (primary), tablet, and mobile views

### Key Success Metrics
- Reduce ticket resolution time by 30%
- Improve agent satisfaction scores
- Achieve 95%+ accessibility compliance
- Support 1920x1080 primary resolution with responsive breakpoints

---

## 🎨 Design System Requirements

### Color Palette

#### Primary Colors (Bank Corporate Identity)
```
Primary Blue:     #003D82 (Bank corporate blue)
Secondary Blue:   #0066CC (Interactive elements)
Accent Blue:      #4A90E2 (Highlights, links)
Dark Navy:        #001F3F (Headers, text)
```

#### Status Colors
```
Critical/High:    #E74C3C (Red - urgent tickets)
Warning/Medium:   #F39C12 (Orange - medium priority)
Success/Low:      #27AE60 (Green - resolved, low priority)
Info:             #3498DB (Blue - informational)
```

#### Neutral Colors
```
Background:       #F8F9FA (Light gray)
Surface:          #FFFFFF (White cards/panels)
Border:           #E1E4E8 (Subtle borders)
Text Primary:     #2C3E50 (Dark gray)
Text Secondary:   #7F8C8D (Medium gray)
Disabled:         #BDC3C7 (Light gray)
```

### Typography

#### Font Family
```
Primary: 'Inter', 'Segoe UI', system-ui, sans-serif
Monospace: 'Roboto Mono', 'Courier New', monospace (for ticket numbers)
```

#### Font Sizes & Weights
```
H1: 32px / Bold (600)      - Page titles
H2: 24px / Semibold (600)  - Section headers
H3: 18px / Semibold (600)  - Card titles
Body: 14px / Regular (400) - Main content
Small: 12px / Regular (400) - Labels, metadata
Tiny: 10px / Regular (400)  - Timestamps, footnotes
```

### Spacing System
```
xs:  4px   - Tight spacing
sm:  8px   - Small gaps
md:  16px  - Standard spacing
lg:  24px  - Section spacing
xl:  32px  - Large gaps
2xl: 48px  - Major sections
```

### Border Radius
```
Small:  4px  - Badges, tags
Medium: 8px  - Buttons, inputs
Large:  12px - Cards, panels
XLarge: 16px - Modal dialogs
```

### Shadows
```
Small:  0 1px 3px rgba(0,0,0,0.12)
Medium: 0 4px 6px rgba(0,0,0,0.1)
Large:  0 10px 20px rgba(0,0,0,0.15)
```

---

## 📱 Screen Layouts & Components

### 1. Dashboard Screen (Primary View)

#### Layout Structure
```
┌─────────────────────────────────────────────────────┐
│ Top Navigation Bar (64px height)                    │
├─────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│ │ Stat Card 1 │ │ Stat Card 2 │ │ Stat Card 3 │   │
│ │ Open: 24    │ │ Progress: 8 │ │ Resolved: 45│   │
│ └─────────────┘ └─────────────┘ └─────────────┘   │
│                                                      │
│ ┌───────────────────────────────────────────────┐  │
│ │ Active Tickets Table                          │  │
│ │ [Filters] [Search] [Sort]                     │  │
│ │ ┌──────────────────────────────────────────┐ │  │
│ │ │ Ticket rows with status badges           │ │  │
│ │ └──────────────────────────────────────────┘ │  │
│ └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

#### Components Required

**A. Top Navigation Bar**
- **Dimensions**: Full width × 64px height
- **Elements**:
  - Bank logo (left, 40px height)
  - Application title "Customer Service Ticketing"
  - Search bar (center, 400px width)
  - Notification bell icon with badge
  - User profile dropdown (right)
- **Background**: White with bottom border (#E1E4E8)
- **Shadow**: Small shadow for depth

**B. Statistics Cards (4 cards)**
- **Dimensions**: Flexible width (grid: 4 columns on desktop)
- **Height**: 120px
- **Content**:
  - Icon (32px, colored by status)
  - Label (12px, uppercase, gray)
  - Number (48px, bold, colored)
  - Trend indicator (optional: ↑ 12% from last week)
- **States**: Default, Hover (lift effect)
- **Cards**:
  1. Open Tickets (Red icon)
  2. In Progress (Orange icon)
  3. Resolved Today (Green icon)
  4. Total Customers (Blue icon)

**C. Active Tickets Table**
- **Container**: White card with border radius 12px
- **Header**:
  - Title "Active Tickets" (H2)
  - Filter dropdown (Status, Priority, Category)
  - Search input (with icon)
  - Sort options
  - "New Ticket" button (primary blue)
- **Table Columns**:
  1. Ticket # (monospace, bold, clickable)
  2. Customer Name (with avatar)
  3. Subject (truncated with tooltip)
  4. Category (badge)
  5. Priority (colored badge)
  6. Status (colored badge)
  7. Assigned To (with avatar)
  8. Created Date (relative time)
  9. Actions (3-dot menu)
- **Row States**: Default, Hover, Selected
- **Pagination**: Bottom, showing "1-10 of 156"

### 2. Ticket Detail View (Modal/Side Panel)

#### Layout
```
┌─────────────────────────────────────┐
│ [X] Ticket #TKT-2024-001234         │
├─────────────────────────────────────┤
│ Customer Info Card                  │
│ ┌─────────────────────────────────┐ │
│ │ 👤 John Doe                     │ │
│ │ 📧 john.doe@email.com           │ │
│ │ 📱 +62-812-3456-7890            │ │
│ │ 🏦 Account: SAVINGS             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Ticket Details                      │
│ ┌─────────────────────────────────┐ │
│ │ Subject: [text]                 │ │
│ │ Category: [badge]               │ │
│ │ Priority: [badge]               │ │
│ │ Status: [badge]                 │ │
│ │ Description: [text area]        │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Activity Timeline                   │
│ ┌─────────────────────────────────┐ │
│ │ ● Created - 2 hours ago         │ │
│ │ ● Assigned to Agent - 1h ago    │ │
│ │ ● Status changed - 30m ago      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Update Status] [Add Note] [Close]  │
└─────────────────────────────────────┘
```

#### Components

**A. Modal/Panel Container**
- **Width**: 600px (modal) or 400px (side panel)
- **Height**: Full height or auto
- **Background**: White
- **Shadow**: Large shadow
- **Animation**: Slide in from right

**B. Customer Info Card**
- **Background**: Light blue (#F0F7FF)
- **Border**: 1px solid #D0E4FF
- **Padding**: 16px
- **Elements**:
  - Avatar (48px circle)
  - Name (16px, bold)
  - Contact details (icons + text)
  - Account type badge

**C. Ticket Details Section**
- **Form Fields**:
  - Subject (read-only or editable)
  - Category dropdown with icons
  - Priority selector (radio buttons with colors)
  - Status dropdown
  - Description textarea (expandable)
- **Field States**: Default, Focus, Disabled, Error

**D. Activity Timeline**
- **Style**: Vertical timeline with dots
- **Items**:
  - Timestamp (relative)
  - Action description
  - User avatar (small, 24px)
  - Color-coded by action type

**E. Action Buttons**
- **Primary**: "Update Status" (blue)
- **Secondary**: "Add Note" (gray outline)
- **Danger**: "Close Ticket" (red outline)

### 3. Create New Ticket Form

#### Layout
```
┌─────────────────────────────────────┐
│ Create New Ticket                   │
├─────────────────────────────────────┤
│ Step 1: Customer Selection          │
│ ┌─────────────────────────────────┐ │
│ │ Search customer...              │ │
│ │ [Dropdown with search]          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Step 2: Ticket Information          │
│ ┌─────────────────────────────────┐ │
│ │ Subject: [input]                │ │
│ │ Category: [dropdown]            │ │
│ │ Priority: [radio buttons]       │ │
│ │ Description: [textarea]         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Cancel] [Create Ticket]            │
└─────────────────────────────────────┘
```

#### Components

**A. Multi-step Form**
- **Progress Indicator**: 2 steps with visual progress
- **Validation**: Real-time with error messages
- **Required Fields**: Marked with asterisk (*)

**B. Customer Search**
- **Type**: Autocomplete dropdown
- **Features**:
  - Search by name, email, or customer ID
  - Show avatar + name + ID in results
  - Recent customers quick access

**C. Category Dropdown**
- **Options**:
  - 🏦 Account Issue
  - 💳 Transaction Dispute
  - 💰 Card Issue
  - 📊 Loan Inquiry
  - ❓ General
- **Icons**: Colored icons for each category

**D. Priority Selector**
- **Type**: Radio button group (horizontal)
- **Options**:
  - 🔴 Critical
  - 🟠 High
  - 🟡 Medium
  - 🟢 Low
- **Visual**: Color-coded circles with labels

### 4. Customer Management Screen

#### Layout
```
┌─────────────────────────────────────┐
│ Customers                           │
│ [Search] [Filter] [+ New Customer]  │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ Customer Cards Grid             │ │
│ │ ┌──────┐ ┌──────┐ ┌──────┐     │ │
│ │ │ Card │ │ Card │ │ Card │     │ │
│ │ └──────┘ └──────┘ └──────┘     │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Components

**A. Customer Card**
- **Dimensions**: 300px × 180px
- **Content**:
  - Avatar (64px)
  - Name (16px, bold)
  - Customer ID (12px, monospace)
  - Email & Phone (12px, with icons)
  - Account type badge
  - Active status indicator
  - "View Details" button
- **States**: Default, Hover (shadow increase)

---

## 🎭 Component States & Interactions

### Button States
```
Default:  Background color, no shadow
Hover:    Darker background, small shadow
Active:   Pressed effect (scale 0.98)
Disabled: Gray background, reduced opacity
Loading:  Spinner icon, disabled state
```

### Input Field States
```
Default:  Gray border, white background
Focus:    Blue border (2px), subtle shadow
Error:    Red border, error message below
Success:  Green border, checkmark icon
Disabled: Gray background, no interaction
```

### Badge Styles

#### Status Badges
```
OPEN:        Red background (#FFEBEE), red text (#C62828)
IN_PROGRESS: Orange background (#FFF3E0), orange text (#F57C00)
RESOLVED:    Green background (#E8F5E9), green text (#388E3C)
CLOSED:      Gray background (#F5F5F5), gray text (#616161)
PENDING:     Yellow background (#FFF9C4), yellow text (#F57F17)
```

#### Priority Badges
```
CRITICAL: Dark red (#B71C1C), white text
HIGH:     Red (#E74C3C), white text
MEDIUM:   Orange (#F39C12), white text
LOW:      Green (#27AE60), white text
```

#### Category Badges
```
Rounded corners (16px)
Icon + Text
Colored background (light)
Colored text (dark)
```

### Table Row Interactions
```
Default:  White background
Hover:    Light gray background (#F8F9FA)
Selected: Light blue background (#E3F2FD)
Clicked:  Navigate to detail view
```

---

## 📐 Responsive Breakpoints

### Desktop (Primary)
- **Width**: 1920px × 1080px
- **Layout**: Full multi-column layout
- **Sidebar**: Visible, 240px width

### Laptop
- **Width**: 1366px × 768px
- **Layout**: Adjusted column widths
- **Sidebar**: Collapsible

### Tablet
- **Width**: 768px × 1024px
- **Layout**: 2-column grid for cards
- **Sidebar**: Hidden, hamburger menu
- **Table**: Horizontal scroll

### Mobile
- **Width**: 375px × 667px
- **Layout**: Single column, stacked
- **Table**: Card view instead of table
- **Navigation**: Bottom tab bar

---

## ♿ Accessibility Requirements

### WCAG 2.1 AA Compliance

#### Color Contrast
- **Text**: Minimum 4.5:1 ratio for normal text
- **Large Text**: Minimum 3:1 ratio (18px+ or 14px+ bold)
- **Interactive Elements**: Minimum 3:1 ratio for borders/icons

#### Keyboard Navigation
- **Tab Order**: Logical flow through all interactive elements
- **Focus Indicators**: Visible 2px blue outline on all focusable elements
- **Shortcuts**: Keyboard shortcuts for common actions
  - `Ctrl+N`: New ticket
  - `Ctrl+F`: Search
  - `Esc`: Close modal

#### Screen Reader Support
- **ARIA Labels**: All icons and buttons
- **Alt Text**: All images and avatars
- **Live Regions**: Status updates announced
- **Semantic HTML**: Proper heading hierarchy

#### Interactive Elements
- **Minimum Size**: 44×44px touch targets
- **Spacing**: 8px minimum between clickable elements
- **Error Messages**: Clear, descriptive, associated with fields

---

## 🎬 Animations & Transitions

### Micro-interactions
```
Button Hover:     150ms ease-in-out
Modal Open:       300ms slide-in from right
Card Hover:       200ms transform scale(1.02)
Loading Spinner:  Continuous rotation
Toast Messages:   300ms slide-down, auto-dismiss 5s
```

### Page Transitions
```
Route Change:     200ms fade
Tab Switch:       150ms fade
Dropdown Open:    200ms ease-out
```

### Loading States
```
Skeleton Screens: Shimmer animation for content loading
Progress Bars:    Smooth width transition
Spinners:         Rotating circle (primary color)
```

---

## 📊 Data Visualization

### Charts & Graphs (Future Enhancement)
- **Ticket Volume**: Line chart showing daily ticket creation
- **Resolution Time**: Bar chart by category
- **Agent Performance**: Horizontal bar chart
- **Status Distribution**: Donut chart

### Chart Styling
- **Colors**: Use status color palette
- **Tooltips**: White background, shadow, rounded corners
- **Legends**: Positioned below or right of chart
- **Responsive**: Scale appropriately on smaller screens

---

## 🔔 Notifications & Alerts

### Toast Notifications
- **Position**: Top-right corner
- **Width**: 360px
- **Types**:
  - Success (green icon)
  - Error (red icon)
  - Warning (orange icon)
  - Info (blue icon)
- **Duration**: 5 seconds auto-dismiss
- **Action**: Optional action button

### In-app Notifications
- **Bell Icon**: Badge with count
- **Dropdown**: List of recent notifications
- **Types**:
  - New ticket assigned
  - Ticket status changed
  - Customer replied
  - SLA warning

---

## 📝 Forms & Validation

### Input Validation
- **Real-time**: Validate on blur
- **Error Messages**: Below field, red text, icon
- **Success Indicators**: Green checkmark icon
- **Required Fields**: Red asterisk (*)

### Form Patterns
- **Inline Editing**: Click to edit in tables
- **Auto-save**: Draft tickets saved automatically
- **Confirmation**: Modal for destructive actions

---

## 🖼️ Icons & Imagery

### Icon Library
- **Recommended**: Heroicons, Lucide, or Feather Icons
- **Style**: Outline style for consistency
- **Size**: 16px, 20px, 24px variants
- **Color**: Inherit from parent or status color

### Common Icons Needed
```
🎫 Ticket
👤 User/Customer
📧 Email
📱 Phone
🏦 Bank/Account
💳 Card
📊 Dashboard
🔔 Notification
⚙️ Settings
🔍 Search
➕ Add/Create
✏️ Edit
🗑️ Delete
✓ Success
✗ Error
⚠️ Warning
ℹ️ Info
```

### Avatar Images
- **Default**: Initials on colored background
- **Size**: 24px, 32px, 48px, 64px variants
- **Shape**: Circle
- **Fallback**: User icon if no image

---

## 📱 Mobile-Specific Considerations

### Touch Interactions
- **Swipe**: Swipe left on ticket row for quick actions
- **Pull to Refresh**: Dashboard and lists
- **Long Press**: Context menu on tickets

### Mobile Navigation
- **Bottom Tab Bar**: 5 main sections
  - Dashboard
  - Tickets
  - Customers
  - Notifications
  - Profile

### Mobile Optimizations
- **Simplified Tables**: Card view instead of table
- **Collapsible Sections**: Accordion for details
- **Floating Action Button**: Quick create ticket

---

## 🎨 Figma File Structure

### Recommended Page Organization
```
1. 📘 Cover & Overview
2. 🎨 Design System
   - Colors
   - Typography
   - Spacing
   - Components
3. 🖥️ Desktop Screens
   - Dashboard
   - Ticket List
   - Ticket Detail
   - Create Ticket
   - Customer Management
4. 📱 Mobile Screens
   - Mobile Dashboard
   - Mobile Ticket List
   - Mobile Ticket Detail
5. 🧩 Components Library
   - Buttons
   - Inputs
   - Cards
   - Badges
   - Modals
   - Tables
6. 🎭 States & Variations
7. 📐 Responsive Layouts
```

### Component Naming Convention
```
Component/Variant/State
Example: Button/Primary/Hover
         Card/Ticket/Selected
         Badge/Status/Open
```

---

## 🚀 Implementation Notes

### Design Handoff Requirements
1. **Figma File**: Organized with proper naming
2. **Design Tokens**: Export as JSON for developers
3. **Assets**: Export icons as SVG, images as PNG/WebP
4. **Specifications**: Spacing, sizing, colors documented
5. **Prototypes**: Interactive flows for key user journeys

### Developer Collaboration
- **Design System**: Create shared component library
- **Responsive Specs**: Provide breakpoint specifications
- **Animation Specs**: Document timing and easing functions
- **Accessibility Notes**: ARIA labels and keyboard navigation

### Future Enhancements
- Dark mode support
- Advanced filtering and search
- Bulk actions on tickets
- Email integration preview
- Real-time collaboration features
- Analytics dashboard

---

## ✅ Design Checklist

### Before Handoff
- [ ] All screens designed for desktop (1920×1080)
- [ ] Mobile versions created (375×667)
- [ ] Component library complete
- [ ] Color contrast checked (WCAG AA)
- [ ] Interactive prototype created
- [ ] All states documented (hover, active, disabled)
- [ ] Responsive breakpoints defined
- [ ] Icons and assets exported
- [ ] Design tokens documented
- [ ] Accessibility annotations added

### Quality Assurance
- [ ] Consistent spacing throughout
- [ ] Typography hierarchy clear
- [ ] Color usage consistent
- [ ] All interactive elements have hover states
- [ ] Error states designed
- [ ] Loading states designed
- [ ] Empty states designed
- [ ] Success messages designed

---

## 📞 Contact & Questions

For questions about these requirements or design clarifications:
- **Product Owner**: [Name]
- **UX Designer**: [Name]
- **Development Lead**: [Name]

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Status**: Ready for Design Phase  
**Next Review**: After initial mockups completed