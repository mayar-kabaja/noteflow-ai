# Creating Social Media Preview Image

When you share your VoiceNotes AI link on social media, WhatsApp, Slack, or other platforms, this preview image will appear.

## Current Setup

A basic SVG preview image is included at `static/images/social-preview.svg`

## Creating a Custom PNG Image (Recommended)

For better compatibility across all platforms, create a PNG version:

### Option 1: Use Online Tools (Easiest)

1. Visit [Canva](https://www.canva.com/) (free)
2. Create a custom size: **1200 x 630 pixels**
3. Use this template idea:
   - Background: Purple gradient (#667eea to #764ba2)
   - Large microphone emoji 🎤 in center
   - Title: "VoiceNotes AI" (large, bold, white)
   - Subtitle: "Transform Voice Notes into Structured Meeting Minutes"
   - Icons: ✨ AI Transcription • 📝 Smart Summaries • 🌐 Multi-Language
4. Download as PNG
5. Save as `static/images/social-preview.png`

### Option 2: Use Figma (Professional)

1. Visit [Figma](https://www.figma.com/) (free)
2. Create a frame: 1200 x 630 pixels
3. Design your preview
4. Export as PNG @ 2x for crisp quality
5. Save as `static/images/social-preview.png`

### Option 3: Convert Existing SVG

If you have ImageMagick installed:

```bash
cd static/images
convert social-preview.svg social-preview.png
```

### Option 4: AI-Generated Image

Use AI tools like:
- [DALL-E](https://openai.com/dall-e-2)
- [Midjourney](https://www.midjourney.com/)
- [Stable Diffusion](https://stability.ai/)

Prompt: "Modern, minimalist app preview image for voice transcription AI app, purple gradient background, microphone icon, clean typography, 1200x630 pixels"

## Image Requirements

- **Dimensions**: 1200 x 630 pixels (mandatory for Facebook/LinkedIn)
- **Format**: PNG or JPG (PNG recommended for transparency)
- **Size**: Under 5MB (ideally under 1MB)
- **Text**: Large and readable (will be scaled down in previews)
- **Safe zone**: Keep important content in center 1200x600 area

## Testing Your Preview

After adding your image, test how it looks:

1. **Facebook Debugger**: https://developers.facebook.com/tools/debug/
2. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
3. **LinkedIn Post Inspector**: https://www.linkedin.com/post-inspector/
4. **WhatsApp**: Just send the link to yourself

## Quick Design Tips

- Use your brand colors (currently purple gradient)
- Include the app icon/logo
- Show key features or benefits
- Keep text minimal and large
- Use high contrast for readability
- Test on mobile preview size

## Updating the Image

Once you have `social-preview.png`, update `templates/base.html`:

Change:
```html
<meta property="og:image" content="{{ url_for('static', filename='images/social-preview.svg', _external=True) }}">
```

To:
```html
<meta property="og:image" content="{{ url_for('static', filename='images/social-preview.png', _external=True) }}">
```

And same for the Twitter image tag.

## Current Preview

Your current SVG preview shows:
- 🎤 Microphone icon
- "VoiceNotes AI" title
- Subtitle with app description
- Feature highlights
- Purple gradient background

Feel free to customize `static/images/social-preview.svg` or replace with PNG!
