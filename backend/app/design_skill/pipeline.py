from app.design_skill.models import PipelineStep


PIPELINE_STEPS = [
    PipelineStep(
        number="01",
        phase="Brief & Strategy",
        title="Brief and Copywriting",
        purpose="Define brand, audience, tone, and page copy before touching code.",
        tools=["Perplexity", "Claude.ai"],
    ),
    PipelineStep(
        number="02",
        phase="Reference",
        title="Find a Section Reference",
        purpose="Collect strong hero and layout references from design galleries.",
        tools=["Dribbble", "Behance", "Awwwards"],
    ),
    PipelineStep(
        number="03",
        phase="Reference",
        title="Strip the Background",
        purpose="Create a clean black-and-white UI reference that preserves layout only.",
        tools=["GPT Image", "OpenArt"],
    ),
    PipelineStep(
        number="04",
        phase="Build",
        title="Recreate the Layout",
        purpose="Use the clean reference to build a pixel-close working template.",
        tools=["Claude Code", "Next.js", "React Spring"],
    ),
    PipelineStep(
        number="05",
        phase="Fonts & Color",
        title="Typography",
        purpose="Pick expressive display fonts and a readable functional family.",
        tools=["Google Fonts", "Awwwards Free Fonts"],
    ),
    PipelineStep(
        number="06",
        phase="Fonts & Color",
        title="Color Palettes",
        purpose="Translate a strong palette into CSS custom properties.",
        tools=["Coolors"],
    ),
    PipelineStep(
        number="07",
        phase="3D Models",
        title="3D Models",
        purpose="Add GLB/GLTF objects through Three.js or Spline when useful.",
        tools=["Sketchfab", "Three.js", "Spline"],
    ),
    PipelineStep(
        number="08",
        phase="Visual Assets",
        title="Image and Video Generation",
        purpose="Generate hero imagery, 3D renders, and looping backgrounds.",
        tools=["OpenArt", "Kling"],
    ),
    PipelineStep(
        number="09",
        phase="Animations",
        title="Animation References",
        purpose="Implement hover, scroll, marquee, and entrance references.",
        tools=["Pinterest", "GSAP", "Framer Motion"],
    ),
    PipelineStep(
        number="10",
        phase="Optimization",
        title="Asset Compression",
        purpose="Convert images, compress video, preload fonts, and prevent layout shift.",
        tools=["Squoosh", "Lighthouse"],
    ),
    PipelineStep(
        number="11",
        phase="Deploy",
        title="Host the Site",
        purpose="Deploy to Vercel or Netlify and connect a custom domain.",
        tools=["Vercel", "Netlify", "Hostinger"],
    ),
]

