# Design System Direction

This is a product direction, not a mandate to overwrite an existing design system. If the repository already contains a coherent visual language, inspect it and extend it consistently.

## Product feel

- Modern, calm, focused, trustworthy.
- Productivity/education SaaS rather than a clinical monitoring tool.
- Clear and restrained use of color.
- Prioritize readable analytics and obvious primary actions.

## Suggested visual direction

- Neutral light or dark foundation; choose one consistent theme for the presentation.
- One primary accent color for actions and selected navigation.
- Green/teal for positive progress, amber for caution, red only for errors or meaningful warnings.
- Cards with subtle borders/shadows and consistent corner radii.
- Avoid using color alone to communicate status; pair it with text/icons.

## Typography

- Use a clean sans-serif already available in the project.
- Establish clear levels for page title, section title, card label, metric value, and supporting text.
- Keep chart labels and secondary metadata readable.

## Layout

- Use a consistent spacing scale.
- Keep dashboard KPI cards aligned.
- Use a responsive grid that collapses naturally.
- Keep main content width comfortable on large screens.
- Ensure session controls remain prominent.

## Interaction states

Every interactive element should have:
- Default state.
- Hover state.
- Focus-visible state.
- Active/selected state where relevant.
- Disabled state where relevant.

## Data visualization

- Use Recharts if already installed or add it only if the repository's package manager and setup support it.
- Use consistent colors for attention, focused time, distraction, and goals.
- Do not use chart shapes as decoration; each chart must answer a question.
- Provide tooltips and readable labels.
- Make charts responsive.

## Copy and terminology

Preferred:
- “Estimated attention”
- “Estimated focused time”
- “Potential distraction”
- “Personal baseline”
- “Demo data” / “Simulated”

Avoid:
- “True attention”
- “Mind-reading”
- “AI knows you are focused”
- Claims that webcam signals prove learning or comprehension.
