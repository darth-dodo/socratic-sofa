# Socratic Sofa - Hobby Project Tasks

Fun improvements to make Socratic Sofa even cooler! 🏛️

**Philosophy**: Keep it simple, fun, and experimental. No enterprise bloat!

---

## 🚀 Quick Wins (Weekend Projects)

### Task 2: Streaming Responses ⚡
**Why**: Watch questions appear in real-time instead of waiting
**Time**: 1-2 hours
**Fun Factor**: ⭐⭐⭐⭐⭐

**Quick Steps**:
1. Add `gr.Chatbot` component to Gradio UI
2. Use `yield` to stream partial responses
3. Add a simple progress bar

**Files**:
- `src/socratic_sofa/gradio_app.py`

**Done When**:
- [ ] Questions appear one at a time
- [ ] Has a "Generating..." indicator

---

### Task 6: Docker Setup 🐳
**Why**: "Works on my machine" → "Works everywhere"
**Time**: 30 minutes
**Fun Factor**: ⭐⭐⭐

**Quick Steps**:
1. Create simple Dockerfile
2. Add docker-compose.yml
3. Test with `docker-compose up`

**Files to Create**:
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["uv", "run", "socratic_web"]
```

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "7860:7860"
    env_file: .env
```

**Done When**:
- [ ] `make docker-up` starts the app
- [ ] Can access at localhost:7860

---

### Task 7: UI Polish ✨
**Why**: Make it look awesome!
**Time**: 1-2 hours
**Fun Factor**: ⭐⭐⭐⭐

**Quick Wins**:
- [ ] Add dark mode toggle (CSS only)
- [ ] Add philosophy emojis (🤔 💭 🏛️ ⚖️)
- [ ] Make dialogue sections collapsible
- [ ] Add "Copy to clipboard" buttons
- [ ] Improve mobile layout

**CSS Snippet**:
```css
[data-theme="dark"] {
  background: #1a1a2e;
  color: #eaeaea;
}
```

**Done When**:
- [ ] Looks good on phone
- [ ] Dark mode works
- [ ] Easy to copy dialogue text

---

## 🎯 Medium Efforts (Weekend + Evening)

### Task 8: Export & Share 📤
**Why**: Share cool dialogues with friends!
**Time**: 2-3 hours
**Fun Factor**: ⭐⭐⭐⭐

**Simple Version**:
- [ ] "Download as Markdown" button
- [ ] "Copy shareable link" (paste.bin style)
- [ ] Optional: Basic PDF export

**Libraries**:
```bash
uv add markdown2 qrcode
```

**Done When**:
- [ ] Can download dialogue as .md file
- [ ] Can share a link to dialogue

---

### Task 4: Dialogue History 💾
**Why**: Don't lose cool dialogues!
**Time**: 3-4 hours
**Fun Factor**: ⭐⭐⭐⭐

**Simple Version** (No database! Just files):
- [ ] Save dialogues to `dialogues/` folder with timestamp
- [ ] List recent dialogues in sidebar
- [ ] Click to reload old dialogue
- [ ] Search by topic name

**Implementation**:
```python
# Save to: dialogues/2025-12-16_justice.json
import json
from pathlib import Path

def save_dialogue(topic, stages):
    filename = f"{datetime.now():%Y-%m-%d}_{topic[:20]}.json"
    Path("dialogues").mkdir(exist_ok=True)
    Path(f"dialogues/{filename}").write_text(json.dumps(stages))
```

**Done When**:
- [ ] Past dialogues show in sidebar
- [ ] Can click to reload
- [ ] Searchable by topic

---

### Task 3: Basic Tests 🧪
**Why**: Make sure stuff doesn't break
**Time**: 2 hours
**Fun Factor**: ⭐⭐

**Minimal Test Suite**:
- [ ] Test agent loading from YAML
- [ ] Test crew initialization
- [ ] Test dialogue generation (mocked)
- [ ] Test UI initialization

**Quick Start**:
```bash
uv add pytest
mkdir tests
```

```python
# tests/test_basic.py
def test_agents_load():
    from socratic_sofa.crew import SocraticSofa
    crew = SocraticSofa()
    assert crew.socratic_questioner() is not None

def test_crew_initializes():
    from socratic_sofa.crew import SocraticSofa
    crew = SocraticSofa().crew()
    assert crew is not None
```

**Done When**:
- [ ] `make test` passes
- [ ] At least 3-5 basic tests

---

## 💡 Experimental Ideas (When You're Feeling Creative)

### Interactive Mode 🗣️
**Turn it into a real dialogue!**

Instead of AI talking to itself, the AI asks YOU questions:

```
AI: "What do you mean by 'justice'?"
You: [Type answer]
AI: "Interesting. And would that apply to..."
```

**Quick Hack**:
- Use `gr.Chatbot` component
- After each AI question, wait for user input
- Continue based on user's answer

**Time**: 2-3 hours
**Fun Factor**: ⭐⭐⭐⭐⭐

---

### Philosopher Personas 🎭
**Choose your philosopher!**

Dropdown to select:
- 🏛️ Socrates (Classic questioning)
- 📚 Plato (Idealist approach)
- 🔬 Aristotle (Empirical focus)
- 🎩 Kant (Deontological)

Just modify the agent's backstory based on selection!

**Time**: 1 hour
**Fun Factor**: ⭐⭐⭐⭐

---

### Topic Library 📚
**Pre-loaded interesting topics**

Add a dropdown with classics:
- "What is justice?"
- "Can we know anything for certain?"
- "Is free will an illusion?"
- "What makes a good life?"

**Time**: 30 minutes
**Fun Factor**: ⭐⭐⭐

---

### Voice Mode 🎙️
**Talk to Socrates!**

Use browser's speech recognition + TTS:
- Speak your answers
- AI speaks questions back

**Libraries**:
```bash
uv add pyttsx3  # Text-to-speech
```

**Time**: 2-3 hours (if you want to experiment)
**Fun Factor**: ⭐⭐⭐⭐⭐

---

## 📋 Current Sprint (Pick 1-2)

**This Weekend**:
- [ ] Task 7: UI Polish (quick & visible)
- [ ] Task 2: Streaming (cool effect)

**Next Weekend**:
- [ ] Task 4: History (useful feature)
- [ ] Task 8: Export (share with friends)

**When Motivated**:
- [ ] Interactive Mode (game changer!)
- [ ] Philosopher Personas (fun variety)

---

## 🎯 Success = Having Fun!

- ✅ Don't stress about perfect code
- ✅ Experiment and try things
- ✅ Share cool dialogues with friends
- ✅ Learn something about philosophy AND coding
- ✅ Keep it simple and maintainable

**Remember**: This is a hobby project. If it stops being fun, take a break! 🌟

---

## 🛠️ Makefile Shortcuts

Add these to make life easier:

```makefile
quick-test:  ## Run just the basic tests
	uv run pytest tests/test_basic.py -v

docker-shell:  ## Jump into Docker container
	docker-compose exec app bash

pretty:  ## Auto-format everything
	uv run ruff format src/

demo:  ## Generate a demo dialogue
	uv run socratic_sofa --topic "What is happiness?"
```

---

**Last Updated**: 2025-12-16
**Vibe**: Hobby Project, Keep It Fun! 🎉
