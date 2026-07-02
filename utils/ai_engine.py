"""
Core Generative AI engine for LinkedIn Content Studio.
Supports OpenAI-compatible APIs (OpenAI / Grok / any compatible endpoint).
Falls back to a smart template-based DEMO MODE when no API key is set,
so the app is fully usable out of the box for everyone.
"""

import os
import random
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------
# API CONFIG
# ---------------------------------------------------------------------
def get_api_key():
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("GROK_API_KEY") or ""


def is_live_mode():
    return bool(get_api_key())


def call_llm(prompt: str, system: str = "", max_tokens: int = 600) -> str:
    """
    Calls OpenAI-compatible chat completion endpoint.
    Returns generated text, or raises on failure (caller should catch
    and fall back to demo mode).
    """
    import requests

    api_key = get_api_key()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.9}

    resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------------
# DEMO MODE TEMPLATE BANKS
# ---------------------------------------------------------------------

HOOKS = [
    "Nobody tells you this about {topic}, but here it is:",
    "I spent 6 months figuring out {topic}. Here's what I learned.",
    "Unpopular opinion about {topic}:",
    "3 years ago I knew nothing about {topic}. Today, here's my biggest lesson.",
    "Stop doing {topic} the hard way. Here's a better approach.",
    "This one mistake in {topic} cost me weeks of work.",
    "Everyone talks about {topic}. Almost nobody talks about this part.",
    "{topic} changed the way I think about my career.",
]

TONE_STYLES = {
    "Professional": {
        "closer": "Curious how others are approaching this — let's discuss in the comments.",
        "voice": "clear, confident, and value-driven",
    },
    "Casual": {
        "closer": "Anyway, that's my two cents 😅 What's your take?",
        "voice": "relaxed, conversational, and personal",
    },
    "Inspirational": {
        "closer": "If you're on a similar journey — keep going. It's worth it.",
        "voice": "motivational and story-driven",
    },
    "Bold/Contrarian": {
        "closer": "Disagree? Let's talk about it in the comments 👇",
        "voice": "direct, opinionated, and thought-provoking",
    },
}

POST_TYPE_BODY = {
    "Achievement": (
        "After weeks of hard work, I finally {topic_action}.\n\n"
        "It wasn't easy — there were moments I wanted to give up. "
        "But breaking it into small, consistent steps made all the difference.\n\n"
        "Key takeaways:\n"
        "→ Consistency beats intensity\n"
        "→ Ask for help early, not after you're stuck\n"
        "→ Document your progress — future you will thank you\n"
    ),
    "Tips/How-To": (
        "Here are {n} things I wish I knew before starting with {topic}:\n\n"
        "1. Start small — don't try to master everything on day one\n"
        "2. Build in public — feedback early saves time later\n"
        "3. Focus on fundamentals before tools/frameworks\n"
        "4. Consistency compounds — small daily effort wins\n"
    ),
    "Story": (
        "A few months ago, I was completely stuck with {topic}.\n\n"
        "I remember staring at my screen thinking 'maybe this isn't for me.'\n\n"
        "But instead of quitting, I broke the problem down, asked for feedback, "
        "and kept iterating.\n\n"
        "Today, that same struggle is one of my proudest wins.\n"
    ),
    "Thought Leadership": (
        "Here's something I've been thinking about in {topic}:\n\n"
        "Most people focus on tools and trends. Few focus on fundamentals "
        "and first principles.\n\n"
        "The people who win long-term are the ones who understand *why* "
        "something works — not just *how* to use it.\n"
    ),
    "Announcement": (
        "🚀 Excited to share something I've been working on: {topic}!\n\n"
        "This has been a journey of learning, iterating, and pushing through "
        "challenges — and I'm proud of where it landed.\n\n"
        "Would love your thoughts and feedback!\n"
    ),
}

HASHTAG_BANK = {
    "ai": ["#ArtificialIntelligence", "#MachineLearning", "#AI", "#DataScience", "#DeepLearning", "#GenerativeAI", "#TechInnovation"],
    "career": ["#CareerGrowth", "#JobSearch", "#PersonalBranding", "#CareerAdvice", "#ProfessionalDevelopment", "#Networking"],
    "student": ["#StudentLife", "#FinalYearProject", "#Learning", "#UniversityLife", "#FreshGraduate", "#StudentJourney"],
    "startup": ["#Startup", "#Entrepreneurship", "#StartupLife", "#BuildInPublic", "#Innovation", "#TechStartup"],
    "marketing": ["#DigitalMarketing", "#ContentMarketing", "#SocialMediaMarketing", "#MarketingStrategy", "#Branding"],
    "software": ["#SoftwareEngineering", "#WebDevelopment", "#Programming", "#Coding", "#TechCommunity", "#DevLife"],
    "general": ["#LinkedInTips", "#Growth", "#Motivation", "#Productivity", "#Leadership", "#Success"],
}


def _pick_hashtag_category(topic: str):
    topic_l = topic.lower()
    for key in HASHTAG_BANK:
        if key in topic_l:
            return key
    if any(w in topic_l for w in ["python", "streamlit", "ml", "model", "neural", "gpt", "llm"]):
        return "ai"
    if any(w in topic_l for w in ["job", "resume", "interview", "hire"]):
        return "career"
    if any(w in topic_l for w in ["fyp", "university", "degree", "semester"]):
        return "student"
    return "general"


# ---------------------------------------------------------------------
# PUBLIC GENERATION FUNCTIONS  (each tries live API, falls back to demo)
# ---------------------------------------------------------------------

def generate_post(topic: str, post_type: str, tone: str, length: str = "Medium") -> dict:
    length_map = {"Short": "under 80 words", "Medium": "120-180 words", "Long": "220-300 words"}
    style = TONE_STYLES.get(tone, TONE_STYLES["Professional"])

    if is_live_mode():
        try:
            system = (
                "You are an expert LinkedIn ghostwriter who writes viral, high-engagement posts. "
                "Use short punchy lines, line breaks, no hashtags in the body, and a strong hook."
            )
            prompt = (
                f"Write a LinkedIn post about: {topic}\n"
                f"Post type: {post_type}\n"
                f"Tone: {tone} ({style['voice']})\n"
                f"Length: {length_map.get(length, 'medium length')}\n"
                f"End with a light call-to-action for comments/engagement."
            )
            text = call_llm(prompt, system=system, max_tokens=500)
            return {"text": text, "mode": "live"}
        except Exception:
            pass  # fall through to demo

    # ---- DEMO MODE ----
    hook = random.choice(HOOKS).format(topic=topic)
    body_template = POST_TYPE_BODY.get(post_type, POST_TYPE_BODY["Tips/How-To"])
    body = body_template.format(topic=topic, topic_action=f"made real progress on {topic}", n=random.choice([3, 4, 5]))
    closer = style["closer"]
    post = f"{hook}\n\n{body}\n{closer}"
    return {"text": post, "mode": "demo"}


def generate_hooks(topic: str, count: int = 6) -> list:
    if is_live_mode():
        try:
            system = "You write scroll-stopping LinkedIn post hooks (first lines). One per line, no numbering."
            prompt = f"Generate {count} different scroll-stopping LinkedIn hook lines about: {topic}"
            text = call_llm(prompt, system=system, max_tokens=300)
            lines = [l.strip("-•123456789. ") for l in text.split("\n") if l.strip()]
            if lines:
                return lines[:count]
        except Exception:
            pass

    pool = [h.format(topic=topic) for h in HOOKS]
    random.shuffle(pool)
    return pool[:count]


def generate_hashtags(topic: str, count: int = 10) -> list:
    if is_live_mode():
        try:
            system = "You suggest relevant, high-reach LinkedIn hashtags. Return only hashtags, space separated."
            prompt = f"Suggest {count} relevant LinkedIn hashtags for a post about: {topic}"
            text = call_llm(prompt, system=system, max_tokens=150)
            tags = re.findall(r"#\w+", text)
            if tags:
                return tags[:count]
        except Exception:
            pass

    category = _pick_hashtag_category(topic)
    tags = HASHTAG_BANK[category][:]
    tags += HASHTAG_BANK["general"]
    words = re.findall(r"[A-Za-z]+", topic)
    custom = ["#" + "".join(w.capitalize() for w in words[:3])] if words else []
    all_tags = list(dict.fromkeys(custom + tags))
    return all_tags[:count]


def generate_carousel(topic: str, slides: int = 6) -> list:
    if is_live_mode():
        try:
            system = "You create LinkedIn carousel content. Return each slide as 'Slide N: Title | Content' on its own line."
            prompt = f"Create a {slides}-slide LinkedIn carousel outline about: {topic}. Keep each slide concise."
            text = call_llm(prompt, system=system, max_tokens=500)
            slides_out = []
            for line in text.split("\n"):
                if "|" in line:
                    title, content = line.split("|", 1)
                    title = re.sub(r"Slide\s*\d+:?", "", title).strip()
                    slides_out.append({"title": title, "content": content.strip()})
            if slides_out:
                return slides_out
        except Exception:
            pass

    # ---- DEMO MODE ----
    demo_structure = [
        ("The Hook", f"Why {topic} matters more than you think"),
        ("The Problem", f"Most people struggle with {topic} because they skip the fundamentals"),
        ("Key Insight #1", "Start with clarity, not complexity"),
        ("Key Insight #2", "Consistency compounds faster than intensity"),
        ("Key Insight #3", "Feedback loops accelerate learning"),
        ("The Takeaway", f"Master {topic} one small step at a time"),
        ("Call To Action", "Follow for more insights like this — and share your thoughts below!"),
    ]
    return [{"title": t, "content": c} for t, c in demo_structure[:slides]]


def optimize_bio(current_bio: str, target_role: str, industry: str) -> dict:
    if is_live_mode():
        try:
            system = "You are a LinkedIn profile optimization expert. Rewrite headlines/bios for maximum recruiter and algorithm visibility."
            prompt = (
                f"Rewrite this LinkedIn headline/about section for a {target_role} in {industry}.\n\n"
                f"Current: {current_bio if current_bio else '(none provided)'}\n\n"
                f"Provide: 1) An optimized one-line headline (under 220 chars), "
                f"2) A short 'About' section (3-4 short paragraphs)."
            )
            text = call_llm(prompt, system=system, max_tokens=500)
            return {"text": text, "mode": "live"}
        except Exception:
            pass

    headline = f"{target_role} | {industry} Enthusiast | Turning Ideas Into Impactful Solutions | Open to Opportunities"
    about = (
        f"I'm a {target_role.lower()} passionate about {industry.lower()}, focused on building "
        f"practical, real-world solutions.\n\n"
        f"My work combines strong fundamentals with a hands-on, iterative approach — "
        f"I believe in learning by building and sharing what I learn along the way.\n\n"
        f"Currently exploring opportunities where I can apply my skills in {industry.lower()} "
        f"to create measurable impact.\n\n"
        f"Let's connect if you're working on something interesting in this space!"
    )
    return {"text": f"HEADLINE:\n{headline}\n\nABOUT:\n{about}", "mode": "demo"}


def generate_content_calendar(theme: str, days: int = 7) -> list:
    pillars = [
        ("Educational", "Share a tip, tutorial, or lesson learned"),
        ("Personal Story", "Share a journey, struggle, or milestone"),
        ("Industry Insight", "Comment on a trend or news in your field"),
        ("Behind the Scenes", "Show your process or work-in-progress"),
        ("Engagement Post", "Ask a question or poll your audience"),
        ("Achievement", "Celebrate a win or milestone"),
        ("Curated/Resource", "Share a useful tool, article, or resource"),
    ]
    calendar = []
    for i in range(days):
        pillar, desc = pillars[i % len(pillars)]
        calendar.append({
            "day": i + 1,
            "pillar": pillar,
            "suggestion": f"{desc} related to {theme}",
        })
    return calendar
