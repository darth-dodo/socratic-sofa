# Web Interface Guide

Welcome to the Socratic Sofa web interface! This guide will help you navigate the platform and get the most out of your philosophical dialogues.

## Overview

The Socratic Sofa web interface provides an intuitive, user-friendly way to engage with AI-powered philosophical dialogues. Built with Gradio, the interface is fully responsive and works seamlessly on desktop, tablet, and mobile devices.

## Getting Started

### Accessing the Interface

1. **Local Installation**: After installing Socratic Sofa, launch the web interface:
   ```bash
   make web
   ```
   Or directly:
   ```bash
   poetry run socratic-web
   ```

2. **Default Access**: The interface opens automatically in your browser at `http://localhost:7860`

3. **Network Access**: The interface is accessible on your local network at `http://0.0.0.0:7860`

### Interface Layout

The web interface consists of several key sections:

```
┌─────────────────────────────────────┐
│  Header & Introduction              │
├─────────────────────────────────────┤
│  How It Works & Method Overview     │
├─────────────────────────────────────┤
│  Topic Selection                    │
│  - Dropdown Library                 │
│  - Custom Topic Input               │
│  - Begin Dialogue Button            │
├─────────────────────────────────────┤
│  Proposed Topic Display             │
├─────────────────────────────────────┤
│  First Inquiry  │  Alternative      │
│  (Proposition)  │  Inquiry          │
│                 │  (Opposition)     │
├─────────────────────────────────────┤
│  Dialectic Evaluation               │
├─────────────────────────────────────┤
│  About & Footer                     │
└─────────────────────────────────────┘
```

## Features

### 1. Topic Selection System

The interface offers two ways to choose your philosophical topic:

#### Option A: Topic Library Dropdown

The dropdown menu contains 100+ curated philosophical questions organized by category:

**What You'll See:**
- **"✨ Let AI choose"**: Allows the AI to select an appropriate topic for exploration
- **[Category] Topic Format**: Each topic is labeled with its category for easy browsing
  - Example: `[Classic Philosophy] What is justice?`
  - Example: `[Modern Dilemmas] Should AI have rights?`

**How to Use:**
1. Click on the dropdown labeled **"📚 Topic Library"**
2. Scroll through the categorized topics
3. Click to select your desired topic
4. The selection automatically populates for the dialogue

**Categories Available:**
- Classic Philosophy
- Ethics & Morality
- Mind & Consciousness
- Society & Politics
- Modern Dilemmas
- Fun & Quirky
- Personal Life
- Big Questions
- Art & Creativity
- Science & Knowledge

#### Option B: Custom Topic Input

For exploring your own philosophical questions:

**What You'll See:**
- A text box labeled **"Or Enter Your Own Topic"**
- Placeholder text: `E.g., 'Should we colonize Mars?'`
- Support for multi-line input (2 lines visible)

**How to Use:**
1. Type your philosophical question directly into the text box
2. Your custom topic takes priority over the dropdown selection
3. Leave empty to use the dropdown selection instead

**Priority Rules:**
- Custom text input always overrides dropdown selection
- If both are filled, the custom input is used
- If custom input is empty, dropdown selection is used
- If both are empty and "✨ Let AI choose" is selected, AI picks a topic

### 2. Content Moderation

The system includes built-in content filtering to ensure philosophical dialogues remain appropriate and constructive:

**What Happens:**
- Topics are automatically checked before processing
- Inappropriate content triggers a helpful message
- Alternative topic suggestions are provided
- No dialogue is generated for filtered content

**User Experience:**
If your topic is filtered, you'll see:
```
⚠️ [Reason for filtering]

**Suggested topics:**
- [Alternative topic 1]
- [Alternative topic 2]
- [Alternative topic 3]
```

### 3. Begin Dialogue Button

**Visual Design:**
- Large, prominent purple button
- Text: **"🧠 Begin Socratic Dialogue"**
- Touch-friendly (minimum 48px height)
- Full width on mobile devices

**What Happens When You Click:**
1. System validates your topic selection
2. Content moderation check runs
3. Progress indicator appears (dialogue generation begins)
4. Takes approximately 2-3 minutes to complete
5. Results populate the output sections automatically

**Important Notes:**
- Each dialogue requires significant processing time
- AI agents work through multiple phases
- Authentic Socratic questioning takes time to develop
- Be patient - quality philosophical inquiry cannot be rushed

### 4. Output Sections

The interface displays results in four distinct sections:

#### A. Proposed Topic (📜)

**Location**: Full-width section below the input area

**What It Shows:**
- The final topic selected or generated by the AI
- Explanation of why this topic was chosen
- Context and philosophical significance
- Initial framing of the question

**Example Content:**
```markdown
# Selected Topic: What is justice?

This classic philosophical question explores the nature of
fairness, moral rightness, and social order...
```

#### B. First Line of Inquiry (🔵 Proposition)

**Location**: Left column of the dialogue outputs

**What It Shows:**
- Initial Socratic exploration of the topic
- Series of probing questions
- Exposure of assumptions
- Progressive questioning technique
- Logical progression toward insight

**Dialogue Structure:**
```markdown
## 🔵 First Line of Inquiry

**Initial Position:** [Starting assumption]

**Question 1:** [First probing question]
- Purpose: [What this question reveals]

**Question 2:** [Follow-up question]
- Purpose: [Deeper exploration]

[Continues through systematic questioning...]
```

**Key Elements:**
- Questions build on previous responses
- Elenchus (refutation through questioning) employed
- Contradictions exposed gently
- No definitive answers provided
- Intellectual humility maintained

#### C. Alternative Line of Inquiry (🟢 Opposition)

**Location**: Right column of the dialogue outputs

**What It Shows:**
- Different angle on the same topic
- Alternative assumptions explored
- Contrasting perspective
- Different questioning approach
- Complementary insights

**Purpose:**
- Shows multiple valid philosophical approaches
- Demonstrates that single topics have many facets
- Encourages broader thinking
- Prevents narrow conclusions

**Visual Layout:**
- Desktop: Side-by-side with Proposition for comparison
- Mobile: Stacked vertically for easy reading

#### D. Dialectic Evaluation (⚖️)

**Location**: Full-width section at the bottom

**What It Shows:**
- Quality assessment of the Socratic dialogue
- Authenticity evaluation
- Effectiveness of questioning technique
- Areas of strong inquiry
- Opportunities for deeper exploration
- Meta-commentary on the philosophical process

**Evaluation Criteria:**
- Did questions follow Socratic method principles?
- Were assumptions properly identified?
- Did the dialogue reveal contradictions?
- Was intellectual humility maintained?
- How effective was the progression of inquiry?

### 5. Mobile-Responsive Design

The interface automatically adapts to your device:

#### Desktop Experience (>768px width)
- Two-column layout for Proposition and Opposition
- Larger text and generous spacing
- Side-by-side comparison viewing
- Full-width input controls

#### Mobile Experience (≤768px width)
- Single-column layout (stacks vertically)
- Optimized typography sizes
- Touch-friendly buttons (48px minimum)
- Full-width controls
- Reduced padding for screen space
- Adjusted heading sizes for readability

**Mobile Optimizations:**
- Responsive font scaling
- Stackable columns
- Touch-optimized buttons
- Reduced margins and padding
- Readable line heights
- Optimized markdown rendering

### 6. Visual Design & Theme

**Color Scheme:**
- Primary: Indigo (purple-blue)
- Secondary: Purple
- Theme: Soft, philosophical aesthetic
- Professional and calming design

**Typography:**
- Clear, readable fonts
- Properly scaled headings
- Optimized line spacing
- Responsive text sizing

**UI Components:**
- Rounded corners for modern look
- Proper spacing between elements
- Clear visual hierarchy
- Professional markdown rendering

## Step-by-Step Workflow

### Complete Dialogue Generation Process

**Step 1: Choose Your Topic** (30 seconds)
- Browse the topic library dropdown
- Or type your own philosophical question
- Consider what genuinely interests you

**Step 2: Review How It Works** (1 minute)
- Understand the Socratic method approach
- Note that questions are emphasized over answers
- Prepare for philosophical inquiry, not debate

**Step 3: Begin Dialogue** (Click button)
- Click "🧠 Begin Socratic Dialogue"
- Wait for processing (2-3 minutes)
- Watch for output sections to populate

**Step 4: Read the Proposed Topic** (1-2 minutes)
- Understand how your topic was framed
- Note the philosophical context provided
- See why this topic matters

**Step 5: Explore First Inquiry** (5-10 minutes)
- Read through the Socratic questions carefully
- Consider how each question builds on previous ones
- Notice contradictions being revealed
- Reflect on your own assumptions

**Step 6: Examine Alternative Inquiry** (5-10 minutes)
- Compare with the first line of inquiry
- See how different angles reveal different insights
- Appreciate the complexity of philosophical questions
- Recognize multiple valid approaches

**Step 7: Study the Evaluation** (3-5 minutes)
- Understand the quality of the dialogue
- Learn from the meta-commentary
- See what made the inquiry effective
- Identify areas for deeper exploration

**Step 8: Reflect and Learn** (Open-ended)
- Consider insights gained
- Question your own assumptions
- Apply Socratic thinking to other areas
- Try another dialogue with related topics

## Tips for Best Results

### Choosing Effective Topics

✅ **Good Topic Examples:**
- "What is justice?" - Clear, fundamental concept
- "Is lying ever justified?" - Specific ethical dilemma
- "Can machines think?" - Concrete philosophical question
- "Should we colonize Mars?" - Modern, debatable issue

❌ **Less Effective Topics:**
- "Tell me about philosophy" - Too broad, not inquiry-focused
- "Kant's categorical imperative" - Too specific/academic
- "Is X better than Y?" - Simple comparison without depth
- Personal advice requests - Not philosophical exploration

### Getting the Most from Dialogues

**Before Starting:**
- Have genuine curiosity about the topic
- Be ready to question your assumptions
- Allocate 15-30 minutes for full experience
- Quiet environment helps deep thinking

**During the Dialogue:**
- Read slowly and thoughtfully
- Pause to consider each question
- Notice your emotional reactions
- Don't rush to conclusions

**After the Dialogue:**
- Journal your insights
- Discuss with friends or study groups
- Explore related topics
- Apply questioning technique to other areas

### Understanding Socratic Method

The interface teaches authentic Socratic questioning:

**What to Expect:**
- Questions, not lectures
- Exposure of contradictions
- Progressive refinement of ideas
- No definitive answers
- Intellectual humility

**What NOT to Expect:**
- Debates or arguments
- Simple yes/no answers
- Persuasion or rhetoric
- Definitive conclusions
- Expert authority claims

## Performance & Technical Details

### System Requirements

**Browser Compatibility:**
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers (iOS Safari, Chrome Mobile)

**Minimum Specifications:**
- Modern web browser (2020+)
- JavaScript enabled
- Internet connection for API calls
- 1920x1080 recommended (works on any size)

### Processing Time

**Typical Dialogue Generation:**
- Topic Selection: Instant
- Content Moderation: < 1 second
- AI Processing: 2-3 minutes
- Results Display: Instant

**Factors Affecting Speed:**
- API response times
- Topic complexity
- Server load
- Network connection

### Data & Privacy

**What Gets Processed:**
- Your selected or custom topic
- Current year (for context)
- Content moderation results

**What Gets Stored:**
- Output markdown files in `outputs/` directory
- Four files per dialogue (topic, proposition, opposition, judgment)
- Files are overwritten with each new dialogue

**What Doesn't Get Stored:**
- No user identification
- No session tracking
- No analytics collection
- No personal data retention

## Troubleshooting

### Common Issues

**Problem: Button doesn't respond**
- Solution: Check internet connection
- Solution: Wait for previous dialogue to complete
- Solution: Refresh page and try again

**Problem: Dialogue takes too long**
- Normal: 2-3 minutes is expected
- Check: Network connection stable?
- Try: Simpler topic if complexity is high

**Problem: Content moderation triggered**
- Review: Topic suggestions provided
- Consider: Why topic might be inappropriate
- Try: Related but more constructive topic

**Problem: Output sections empty**
- Check: Error message in any output section?
- Verify: API credentials configured correctly
- Review: Console for error messages (F12 in browser)

**Problem: Mobile layout issues**
- Try: Refresh page
- Verify: Using modern browser
- Rotate: Device to see if layout adjusts

**Problem: Text too small/large**
- Desktop: Use browser zoom (Ctrl/Cmd + or -)
- Mobile: Should auto-scale, but browser zoom works

### Getting Help

**Resources:**
- Project documentation: `docs/` directory
- Issue tracker: GitHub Issues
- Example dialogues: `outputs/` directory
- Source code: Fully open source

**Reporting Issues:**
1. Note the exact topic used
2. Capture error messages
3. Include browser and device info
4. Check if reproducible

## Advanced Usage

### Integration with CLI

The web interface and CLI can be used together:

1. Generate dialogue via web interface
2. Results saved in `outputs/` directory
3. Access files programmatically
4. Analyze patterns across multiple dialogues

### Batch Processing

For multiple topics:
1. Use CLI for batch operations (see CLI guide)
2. Web interface best for interactive exploration
3. Outputs accessible to both interfaces

### Custom Deployment

The web interface can be deployed:
- **Local Network**: Access from multiple devices
- **Ngrok/Tunneling**: Share temporarily with others
- **Cloud Hosting**: Deploy on Hugging Face Spaces, etc.

See deployment documentation for details.

## Accessibility

### Keyboard Navigation

- **Tab**: Move between controls
- **Enter**: Activate buttons
- **Arrow Keys**: Navigate dropdown
- **Escape**: Close dropdown

### Screen Reader Support

- Semantic HTML structure
- Proper ARIA labels
- Descriptive button text
- Markdown content accessible

### Visual Accessibility

- High contrast text
- Readable font sizes
- Clear visual hierarchy
- No reliance on color alone

## Best Practices

### For Individual Learning

1. **Start Simple**: Begin with familiar topics
2. **Go Deep**: Spend time with each dialogue
3. **Reflect**: Journal insights between dialogues
4. **Compare**: Run same topic multiple times to see variations
5. **Apply**: Use Socratic questioning in daily life

### For Educational Settings

1. **Preparation**: Review topic library in advance
2. **Discussion**: Use as catalyst for classroom dialogue
3. **Analysis**: Compare AI questions with student questions
4. **Practice**: Teach students to formulate Socratic questions
5. **Assessment**: Evaluate quality of questioning, not answers

### For Research & Writing

1. **Brainstorming**: Explore multiple angles of thesis topics
2. **Critical Thinking**: Challenge your own arguments
3. **Counterarguments**: Use opposition inquiry for balance
4. **Depth**: Find assumptions you hadn't considered
5. **Documentation**: Save outputs for reference in writing

## Conclusion

The Socratic Sofa web interface provides an accessible, user-friendly gateway to philosophical inquiry. By combining modern AI technology with ancient Socratic wisdom, it offers a unique learning experience that emphasizes questions over answers and inquiry over assertion.

Take your time, be curious, and enjoy the journey of philosophical exploration.

**Next Steps:**
- [CLI Usage Guide](./cli-usage.md) - Learn command-line options
- [Topic Library Guide](./topic-library.md) - Explore all 100 topics
- [Custom Topics Guide](./custom-topics.md) - Create your own questions
