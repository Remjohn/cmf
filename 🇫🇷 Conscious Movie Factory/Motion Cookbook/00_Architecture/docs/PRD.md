# **📄 PRD.md**

**Product Name:** Motion Cookbook  
**Version:** v1.0 (Foundational)  
**Status:** Canonical Rewrite

---

## **1\. Product Overview**

### **1.1 What We Are Building**

Motion Cookbook is a **scene-based explainer animation system** that automatically generates short, high-quality animated video scenes (5–7 seconds each) for short-form and long-form content.

The system is designed primarily for:

* Coaches  
* Educators  
* Thought leaders  
* Health & personal development creators  
* Media-style explainer content (Vox / MagnetsMedia / Kurzgesagt-lite)

The output is **modular animated scenes** that are assembled downstream (e.g., in CapCut, Premiere, or Final Cut).

This is **not** an end-to-end video editor.  
It is a **motion scene generator**.

---

### **1.2 Core Value Proposition**

“Give us context \+ assets, and we generate 5–7 branded, reusable animated scenes that explain, emphasize, or dramatize your message.”

Key differentiator:

* Deterministic animation  
* Reusable motion templates  
* AI only assists preparation, never animation  
* Consistent brand & motion language at scale

---

## **2\. Problem Statement**

### **2.1 The Current Pain**

Creators want:

* Vox-level explainer animations  
* Consistent visual language  
* High engagement short-form content  
* Fast turnaround  
* Low marginal cost per video

But current options are:

* Manual motion design (slow, expensive)  
* Template editors (rigid, generic)  
* AI video generators (unpredictable, inconsistent)

There is **no system** that:

* Separates *motion logic* from *content*  
* Allows AI to help without breaking brand or quality  
* Produces reusable, deterministic animation scenes

---

### **2.2 Why Now**

* AI image generation is strong enough for layered assets  
* Short-form video requires **repeatable patterns**  
* Motion Canvas enables code-based deterministic animation  
* Creators increasingly assemble videos modularly

---

## **3\. Product Goals**

### **3.1 Primary Goals**

1. Generate **5–7 second animated scenes** automatically  
2. Maintain **strict motion consistency**  
3. Allow **scene reuse across clients**  
4. Support **explainer, storytelling, meme, and news formats**  
5. Integrate seamlessly with CapCut / Premiere workflows

---

### **3.2 Non-Goals**

* Full timeline video editing  
* Audio editing or mixing  
* AI-generated animation curves  
* Freeform generative video

---

## **4\. Target Users**

### **4.1 Primary User**

**Content operators for coaches & educators**

* Running short-form pipelines  
* Producing daily or weekly content  
* Need speed \+ consistency

---

### **4.2 Secondary Users**

* Internal creative teams  
* Agencies  
* Media startups  
* Educational YouTube channels

---

## **5\. Core Concepts (Foundational)**

### **5.1 Scene**

A **Scene** is a rigid, versioned motion structure:

* Fixed duration  
* Fixed spatial layout  
* Fixed animation logic  
* Parameterized content

Scenes are the atomic unit of output.

---

### **5.2 Layer Graph**

A **Layer Graph** is a structured representation of all visual elements:

* RGBA layers  
* Semantic labels  
* Spatial bounds  
* Allowed transformations

Layer Graphs are generated or assembled **before** animation.

---

### **5.3 Motion Tokens**

Motion Tokens are reusable animation primitives:

* FadeIn  
* SlideUp  
* EmphasizePulse  
* GlowOutline  
* CameraPush

They are authored once and reused everywhere.

---

### **5.4 Cookbook Metaphor**

* **Ingredients** → Assets, text, images, cutouts  
* **Recipes** → Scenes  
* **Plating** → Motion Canvas render  
* **Dish** → 5–7s video clip

---

## **6\. System Architecture (Product-Level)**

### **6.1 High-Level Flow**

1. User provides context \+ assets  
2. AI agents analyze & prepare materials  
3. Scene planner selects scenes  
4. Layer Graphs are constructed  
5. Motion Canvas renders scenes  
6. Clips exported for assembly

---

### **6.2 AI Agent Pipeline (12 Subagents)**

**Key principle:** AI never animates.

Example subagents:

1. Context Analyzer  
2. Script Segmenter  
3. Scene Matcher  
4. Image Generator (Qwen / Wan)  
5. Layer Extractor (SAM / Qwen Layered)  
6. Semantic Tagger  
7. Region Identifier  
8. Asset Cleaner  
9. Text Synthesizer  
10. Scene Parameter Filler  
11. Brand Styler  
12. Validation Agent

Each agent has:

* Narrow responsibility  
* Deterministic output schema  
* Validation rules

---

## **7\. Models & External Systems**

### **7.1 Image & Layer Models**

Used only for **preparation**:

* **Qwen Image 2512** – image generation  
* **Qwen Image Edit 2511** – controlled edits  
* **Qwen Image Layered** – layered decomposition  
* **SAM 3** – region segmentation  
* **NanoBanana Pro** – complex diagrams & maps

---

### **7.2 Video / FX Assets**

* **Wan Alpha** – alpha-channel FX (smoke, energy, particles)  
* **Z-Image Turbo** – fast image generation  
* **ComfyUI (RunPod)** – advanced workflows (optional)

---

### **7.3 Vision-Language Models**

* **Qwen3-VL**  
* **Wan VLM**

Used for:

* Image understanding  
* Semantic labeling  
* Region selection

---

## **8\. Scene Categories (v1)**

The system launches with **16 core scenes**, grouped into 5 families.

### **8.1 Storytelling Scenes**

* Cutout metaphor scene  
* Before / After juxtaposition  
* Archetype foreshadow

### **8.2 Explainer Scenes**

* Blueprint / flowchart  
* Body map focus  
* Chart reveal  
* Step-by-step path

### **8.3 Emphasis Scenes**

* Affirmation word  
* Kinetic number  
* Misconception → Truth

### **8.4 Social & Meme Scenes**

* Quiz overlay  
* Poll / question card  
* Relatable meme caption

### **8.5 Avatar / Presence Scenes**

* Brand avatar float  
* Mentor quote collage  
* Future-self portrait

---

## **9\. Motion Canvas Role**

Motion Canvas is the **exclusive animation engine**.

It excels at:

* Declarative motion  
* Component-based animation  
* Deterministic rendering  
* Parameterized templates  
* Code review & versioning

Motion Canvas is **not** used for:

* AI decision-making  
* Asset creation  
* Scene planning

---

## **10\. Output Specification**

Each scene outputs:

* MP4 (H.264)  
* 1080×1920  
* Alpha optional (WebM / ProRes later)  
* 5–7 seconds  
* Silent (audio handled downstream)

---

## **11\. UX / Product Interface**

### **11.1 MVP Interface**

* Context input (text)  
* Asset upload (images, logos)  
* Scene selection (auto / manual)  
* Render button  
* Download clips

---

### **11.2 Future Interface**

* Scene preview  
* Parameter tweaking  
* Brand kits  
* Batch rendering  
* API access

---

## **12\. Quality & Constraints**

### **12.1 Determinism**

Same input must always produce the same output.

---

### **12.2 Brand Safety**

* No hallucinated motion  
* No layout drift  
* No font substitution without approval

---

### **12.3 Performance Targets**

* \<30s per scene render (CPU acceptable)  
* Parallel scene rendering  
* Cache reusable assets

---

## **13\. Risks & Mitigations**

| Risk | Mitigation |
| ----- | ----- |
| AI output instability | Strict schemas |
| Motion inconsistency | Motion tokens only |
| Scene creep | Versioned scenes |
| Overcomplexity | Scene-first design |

---

## **14\. Success Metrics**

* Time to first scene \< 10 minutes  
* Reuse rate of scenes \> 70%  
* Engagement uplift vs static B-roll  
* Low revision requests

---

## **15\. Long-Term Vision**

Motion Cookbook becomes:

* A **motion operating system**  
* A **scene marketplace**  
* A **standard for explainer animation automation**

Not “AI video generation” —  
but **AI-assisted motion design at scale**.

---

## **16\. Open Questions (Intentionally Deferred)**

* Real-time preview vs offline render  
* Alpha-first pipeline  
* Marketplace governance  
* Community scene contributions

These are deferred until v2.

---

# **PRD.md \- ADD SECTIONS 17-18**

## **17\. Implementation Roadmap**

### **Phase 1: Foundation (Weeks 1-2) ✅ COMPLETE**

**Objectives:**

* Define system architecture  
* Create all schemas and contracts  
* Establish documentation standards

**Deliverables:**

* ✅ 15 canonical documentation files  
* ✅ Architecture diagrams  
* ✅ Agent contracts  
* ✅ Scene schemas  
* ✅ Motion token library  
* ✅ CLI specification

**Status: 100% Complete**

---

### **Phase 2: MVP Pipeline (Weeks 3-4) 🚧 IN PROGRESS**

**Objectives:**

* Implement core agent pipeline  
* Create 3-5 working scenes  
* Establish testing framework

**Week 3 Deliverables:**

* ✅ CLI implementation (basic)  
* ✅ Orchestrator (sequential pipeline)  
* ✅ 3 core agents (ContextAnalyzer, ScenePlanner, ParameterFiller)  
* ✅ 1 complete scene (RATING\_METER\_1\_TO\_10)  
* ✅ File validation utilities

**Week 4 Deliverables (Current Sprint):**

* 🚧 Complete 6 remaining agents:  
  * AssetValidator (85% done)  
  * LayerExtractor (60% done)  
  * SemanticLabeler (40% done)  
  * TextSynthesizer (0%)  
  * ImageGenerator (0%)  
  * SpeechAnalyzer (0%)  
* 🚧 Implement 2 more scenes:  
  * BEFORE\_AFTER\_SELF\_SCORE (80% done)  
  * BODY\_MAP\_FOCUS (60% done)  
* 📋 Basic test suite (structure exists)  
* 📋 Error handling polish

**Status: 65% Complete**

**Blockers:**

* LayerExtractor Qwen API integration needs completion  
* SemanticLabeler requires VLM model selection  
* SpeechAnalyzer waiting on Librosa integration decision

---

### **Phase 3: Scene Library Expansion (Weeks 5-6) 📋 PLANNED**

**Objectives:**

* Implement remaining 13 scenes  
* Optimize rendering pipeline  
* Add parallel execution

**Week 5 Deliverables:**

* 📋 Implement 6 simple scenes:  
  * CONFIDENCE\_BAR\_LIVE  
  * PROGRESS\_DELTA\_BADGE  
  * KINETIC\_DEFINITION  
  * QUOTE\_CARD  
  * RESPONSE\_CALLOUT\_LOWER\_THIRD  
  * CONSENSUS\_SCORE\_STACK  
* 📋 Parallel rendering (4 workers)  
* 📋 Layer graph caching

**Week 6 Deliverables:**

* 📋 Implement 7 complex scenes:  
  * REACTION\_EMPHASIS\_QUOTE  
  * CUTOUT\_METAPHOR  
  * MISCONCEPTION\_TRUTH  
  * BRAND\_AVATAR\_FLOAT  
  * BLUEPRINT\_FLOW  
  * STEP\_BREAKDOWN  
  * RHYTHMIC\_ABSTRACT  
* 📋 Performance optimization  
* 📋 Comprehensive test coverage

---

### **Phase 4: Testing & Polish (Week 7\) 📋 PLANNED**

**Objectives:**

* Achieve 85%+ test coverage  
* Create golden master suite  
* Performance benchmarking  
* Bug fixes

**Deliverables:**

* 📋 Unit tests for all agents (85% coverage target)  
* 📋 Integration tests for full pipeline  
* 📋 Golden master renders for all 16 scenes  
* 📋 Performance benchmarks  
* 📋 Error handling validation  
* 📋 Edge case testing  
* 📋 Documentation review

---

### **Phase 5: Production Readiness (Week 8\) 📋 PLANNED**

**Objectives:**

* Deployment infrastructure  
* Monitoring & logging  
* User documentation  
* Alpha release

**Deliverables:**

* 📋 Docker containers  
* 📋 CI/CD pipeline (GitHub Actions)  
* 📋 Deployment scripts (local/RunPod/cloud)  
* 📋 Monitoring dashboard  
* 📋 User guide & tutorials  
* 📋 API documentation (if exposed)  
* 📋 Alpha release to 5 users

---

## **18\. Definition of Done (v1.0 Release Criteria)**

### **Core Functionality ✓**

**Pipeline:**

* ✅ All 12 agents implemented and tested  
* ✅ Sequential pipeline working  
* ✅ Parallel rendering (4+ workers)  
* ✅ Error handling & retry logic  
* ✅ Validation at all gates

**Scenes:**

* ✅ All 16 scenes implemented  
* ✅ Each scene has golden master  
* ✅ Scene tests pass  
* ✅ Render time within targets

**Output Quality:**

* ✅ Deterministic rendering  
* ✅ Brand consistency  
* ✅ No visual artifacts  
* ✅ Correct durations (±0.1s tolerance)

---

### **Technical Quality ✓**

**Testing:**

* ✅ 85%+ unit test coverage  
* ✅ Integration tests pass  
* ✅ Golden master regression tests  
* ✅ Performance benchmarks documented

**Code Quality:**

* ✅ All code reviewed  
* ✅ Type hints (Python)  
* ✅ TypeScript strict mode  
* ✅ No critical linting errors  
* ✅ Documentation strings

**Performance:**

* ✅ Simple scenes: \<30s  
* ✅ Complex scenes: \<60s  
* ✅ Full pipeline (6 scenes): \<5 min  
* ✅ Parallel efficiency: \>70%

---

### **Documentation ✓**

**Developer Docs:**

* ✅ Architecture overview  
* ✅ All schemas documented  
* ✅ Agent contracts  
* ✅ Motion tokens  
* ✅ Extending guide  
* ✅ API reference (if applicable)

**User Docs:**

* ✅ Quickstart guide  
* ✅ CLI reference  
* ✅ Troubleshooting  
* ✅ Example workflows  
* ✅ File format guide

**Operational:**

* ✅ Deployment guide  
* ✅ Monitoring setup  
* ✅ Cost model documented

---

### **Production Infrastructure ✓**

**Deployment:**

* ✅ Docker image built  
* ✅ Can run locally  
* ✅ Can run on RunPod  
* ✅ Environment variables documented

**Monitoring:**

* ✅ Logging configured  
* ✅ Error tracking  
* ✅ Performance metrics  
* ✅ Alert thresholds defined

**Security:**

* ✅ API keys handled securely  
* ✅ File permissions correct  
* ✅ No secrets in code  
* ✅ Input validation

---

### **User Validation ✓**

**Alpha Testing:**

* ✅ 5 alpha users onboarded  
* ✅ Each user generates 10+ scenes  
* ✅ Feedback collected  
* ✅ Critical bugs fixed

**Success Criteria:**

* ✅ \<10% failure rate  
* ✅ \<15% revision requests  
* ✅ Time to first scene: \<10 min  
* ✅ User satisfaction: \>7/10

---

## **Release Checklist**

### **Pre-Release (1 week before)**

* \[ \] All tests passing  
* \[ \] Documentation reviewed  
* \[ \] Performance validated  
* \[ \] Security audit  
* \[ \] Alpha user feedback incorporated  
* \[ \] Known issues documented  
* \[ \] Backup/recovery tested

### **Release Day**

* \[ \] Tag release in git  
* \[ \] Build production Docker image  
* \[ \] Deploy to production environment  
* \[ \] Smoke tests pass  
* \[ \] Monitoring active  
* \[ \] Announcement ready  
* \[ \] Support channels open

### **Post-Release (1 week after)**

* \[ \] Monitor error rates  
* \[ \] Collect user feedback  
* \[ \] Prioritize bug fixes  
* \[ \] Plan v1.1 features

---

## **Version Roadmap**

### **v1.0 \- Foundation (Week 8\)**

**Focus:** Core pipeline \+ 16 scenes \+ documentation **Users:** Alpha testers (5-10)

### **v1.1 \- Polish (Week 10\)**

**Focus:** Performance optimization \+ bug fixes **Users:** Early adopters (20-50) **Features:**

* Batch processing  
* Advanced caching  
* Preview mode  
* Template library

### **v1.2 \- Scale (Week 14\)**

**Focus:** Production features **Users:** General availability (100+) **Features:**

* API access  
* Brand kit marketplace  
* Custom scene variants  
* Cloud rendering

### **v2.0 \- Intelligence (Future)**

**Focus:** Advanced AI features **Users:** Power users **Features:**

* Auto scene selection  
* Voice-driven timing  
* Multi-language support  
* Real-time preview  
* Collaborative editing

---

## **Risk Register**

| Risk | Impact | Likelihood | Mitigation |
| ----- | ----- | ----- | ----- |
| Layer extraction unreliable | High | Medium | Fallback to manual layers |
| Rendering too slow | High | Low | Optimize \+ GPU support later |
| Scene quality inconsistent | High | Medium | Golden masters \+ strict validation |
| AI API costs high | Medium | Medium | Cache aggressively |
| User adoption low | High | Low | Strong onboarding \+ examples |
| Documentation gaps | Medium | Low | Regular reviews |

---

## **Open Questions (Deferred to v1.1+)**

1. **Real-time preview?**

   * Defer to v1.1  
   * MVP: Render then review  
2. **Alpha channel pipeline?**

   * Defer to v1.2  
   * MVP: Opaque backgrounds  
3. **Scene marketplace?**

   * Defer to v2.0  
   * MVP: Core 16 scenes only  
4. **API vs CLI?**

   * MVP: CLI only  
   * v1.2: Consider API  
5. **GPU rendering?**

   * Defer to v1.2  
   * MVP: CPU acceptable  
6. **Multi-language?**

   * Defer to v2.0  
   * MVP: English only

---

## **Current Sprint (Week 4\)**

### **This Week's Goals**

1. Complete AssetValidator (15% remaining)  
2. Complete LayerExtractor (40% remaining)  
3. Complete SemanticLabeler (60% remaining)  
4. Implement TextSynthesizer (100% remaining)  
5. Finish BEFORE\_AFTER\_SELF\_SCORE scene (20% remaining)  
6. Advance BODY\_MAP\_FOCUS scene (40% remaining)

### **Next Week's Goals (Week 5\)**

1. Complete all remaining agents  
2. Implement 6 simple scenes  
3. Basic test coverage (50%+)  
4. Performance baseline established

