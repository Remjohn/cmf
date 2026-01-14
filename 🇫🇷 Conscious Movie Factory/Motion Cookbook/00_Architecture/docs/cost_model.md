# **cost\_model.md**

**Purpose:** Economic model for Motion Cookbook  
 **Status:** v1.0

---

## **1\. Cost Philosophy**

Costs must be:

* **Predictable** \- Known before rendering  
* **Bounded** \- Hard limits prevent runaway spending  
* **Scalable** \- Linear cost growth  
* **Transparent** \- Clear breakdown per scene

**Goal:** Optimize for **scene throughput**, not single video quality.

---

## **2\. Cost Categories**

### **2.1 AI Compute**

**Used for:** Asset preparation (image generation, layer extraction, labeling)

### **2.2 Rendering Compute**

**Used for:** Motion Canvas rendering \+ video encoding

### **2.3 Storage & Bandwidth**

**Used for:** Assets, layer graphs, rendered clips

---

## **3\. Per-Scene Cost Breakdown (v1.0)**

### **Base Cost Structure**

| Category | Cost (USD) | Notes |
| ----- | ----- | ----- |
| **AI Preparation** | $0.01 \- $0.05 | Varies by complexity |
| **Motion Canvas Render** | $0.003 \- $0.01 | CPU-based, 30-60s |
| **Video Encoding (FFmpeg)** | \< $0.001 | Negligible |
| **Storage (temp)** | \< $0.001 | Short-lived |
| **Total per scene** | **$0.02 \- $0.06** | **Average: $0.04** |

---

## **4\. AI Cost Breakdown**

### **4.1 Image Generation (Optional)**

| Model | Resolution | Cost per Image | Use Case |
| ----- | ----- | ----- | ----- |
| Qwen Image 2512 | 1024×1024 | $0.015 | General purpose |
| NanoBanana Pro | 1024×1024 | $0.025 | Complex diagrams |
| Z-Image Turbo | 512×512 | $0.005 | Fast stylized |

**Average:** $0.015 per generated image  
 **Scenes requiring generation:** \~30%  
 **Expected cost per scene:** $0.015 × 0.3 \= **$0.0045**

---

### **4.2 Layer Extraction**

| Method | Cost | Speed |
| ----- | ----- | ----- |
| Qwen Image Layered | $0.008 | 2-3s |
| SAM 3 | $0.012 | 3-5s |
| Manual (user-provided) | $0 | N/A |

**Average:** $0.01  
 **Scenes requiring extraction:** \~80%  
 **Expected cost per scene:** $0.01 × 0.8 \= **$0.008**

---

### **4.3 Semantic Labeling**

| Method | Cost | Speed |
| ----- | ----- | ----- |
| Qwen3-VL | $0.004 | 1s |
| Wan VLM | $0.006 | 1.5s |

**Average:** $0.005  
 **Expected cost per scene:** **$0.005**

---

### **4.4 Speech Analysis (Optional)**

| Method | Cost | Speed |
| ----- | ----- | ----- |
| Librosa \+ VAD | Free (local) | 0.5s |
| Cloud Speech API | $0.006 per minute | Variable |

**Average:** $0.003 (using local processing)  
 **Scenes requiring speech analysis:** \~25%  
 **Expected cost per scene:** $0.003 × 0.25 \= **$0.00075**

---

### **Total AI Cost per Scene: $0.018 \- $0.03**

---

## **5\. Rendering Compute Cost**

### **5.1 Motion Canvas Rendering**

| Hardware | Cost per Hour | Avg Scene Render Time | Cost per Scene |
| ----- | ----- | ----- | ----- |
| CPU (8-core) | $0.20 | 45s | $0.0025 |
| GPU (T4) | $0.50 | 20s | $0.0028 |

**Chosen:** CPU rendering (cheaper at current scale)  
 **Cost per scene:** **$0.0025**

---

### **5.2 Video Encoding (FFmpeg)**

**Cost:** Negligible (\< $0.001 per scene)

---

### **Total Rendering Cost per Scene: $0.003**

---

## **6\. Storage & Bandwidth**

### **6.1 Temporary Storage**

| Asset Type | Size | Lifespan | Cost |
| ----- | ----- | ----- | ----- |
| Source images | 1-5 MB | 1 hour | $0.0001 |
| Layer graph JSON | 10 KB | 1 hour | \< $0.0001 |
| Rendered frames | 50-100 MB | 5 min | $0.0005 |
| Final MP4 | 2-5 MB | Persistent | $0.0002 |

**Total storage cost per scene:** **\< $0.001**

---

### **6.2 Bandwidth**

**Negligible:** Internal transfer within same datacenter.

---

## **7\. Total Cost per Scene (Summary)**

| Component | Cost Range |
| ----- | ----- |
| AI Preparation | $0.018 \- $0.03 |
| Rendering | $0.003 |
| Storage | \< $0.001 |
| **TOTAL** | **$0.021 \- $0.034** |

**Average Cost per Scene:** **$0.027 (\~$0.03)**

---

## **8\. Cost Scaling**

### **Per Video (6 scenes)**

* **Cost:** 6 × $0.03 \= **$0.18**

### **Per 100 Videos**

* **Cost:** 100 × $0.18 \= **$18**

### **Per 1,000 Videos**

* **Cost:** 1,000 × $0.18 \= **$180**

### **Per 10,000 Videos**

* **Cost:** 10,000 × $0.18 \= **$1,800**

**Scaling is linear** \- No fixed overhead after setup.

---

## **9\. Cost Reduction Strategies**

### **9.1 Layer Graph Caching**

**Impact:** Reduces layer extraction costs by \~70%

**Implementation:**

* Cache by source image SHA256  
* Reuse across multiple scenes  
* Cache hit rate: \~60% after first month

**Savings:** $0.008 → $0.002 per scene (when cache hit)  
 **Average savings:** $0.008 × 0.6 \= **$0.0048 per scene**

---

### **9.2 Prefer User-Provided Assets**

**Impact:** Eliminates image generation costs

**Savings:** $0.015 per scene (when user provides images)  
 **User adoption:** \~40% of scenes  
 **Average savings:** $0.015 × 0.4 \= **$0.006 per scene**

---

### **9.3 Gate Expensive Models**

**Strategy:** Use cheaper models by default, expensive models on-demand

**Example:**

* Default: Qwen Image Layered ($0.008)  
* Advanced: SAM 3 ($0.012)  
* Only use SAM 3 if:  
  * User explicitly requests  
  * Qwen fails (confidence \< 0.6)

**Savings:** $0.004 per scene

---

### **9.4 Batch Processing**

**Impact:** Reduce orchestration overhead

**Savings:** \~10% reduction in total time (indirect cost savings)

---

### **Total Optimized Cost per Scene: $0.015 \- $0.02**

---

## **10\. Pricing Implications**

### **10.1 Cost-Plus Pricing**

**Target Margin:** 80%  
 **Cost:** $0.03 per scene  
 **Price:** $0.15 per scene

**Per video (6 scenes):** $0.90

---

### **10.2 Subscription Tiers**

| Tier | Scenes/Month | Cost (to us) | Price | Margin |
| ----- | ----- | ----- | ----- | ----- |
| Starter | 50 | $1.50 | $9.99 | 85% |
| Pro | 200 | $6.00 | $29.99 | 80% |
| Business | 1,000 | $30.00 | $99.99 | 70% |

---

### **10.3 Pay-As-You-Go**

**Price:** $0.20 per scene  
 **Margin:** 85%

---

## **11\. Cost Controls**

### **11.1 Hard Limits**

**Per User:**

* Max scenes per request: 10  
* Max requests per hour: 20  
* Max total scenes per day: 100

**System-Wide:**

* Max concurrent renders: 50  
* Queue depth: 500

---

### **11.2 Timeouts**

| Operation | Timeout | Retry |
| ----- | ----- | ----- |
| AI image generation | 30s | 2x |
| Layer extraction | 60s | 1x |
| Scene render | 90s | 0x |

**If timeout exceeded:** Job fails, user notified, no charge.

---

### **11.3 Failure Cost Handling**

**Policy:** Only charge for successful renders.

**Failed render \= $0 charge**

---

## **12\. Cost Monitoring**

### **12.1 Metrics to Track**

* **Per scene cost** (actual vs estimate)  
* **Cache hit rate** (layer graphs)  
* **Model usage distribution** (which AI models used)  
* **Render time P50, P95, P99**  
* **Failure rate** (by scene type)

---

### **12.2 Cost Alerting**

**Triggers:**

* Per scene cost \> $0.05 (alert)  
* Per scene cost \> $0.10 (page)  
* Daily spend \> $500 (alert)  
* Hourly spend \> $100 (alert)

---

## **13\. Profitability Scenarios**

### **Scenario A: 100 Customers, Starter Tier**

**Revenue:** 100 × $9.99 \= $999/month  
 **Cost:** 100 × 50 × $0.03 \= $150/month  
 **Margin:** $849 (85%)

---

### **Scenario B: 50 Customers, Pro Tier**

**Revenue:** 50 × $29.99 \= $1,500/month  
 **Cost:** 50 × 200 × $0.03 \= $300/month  
 **Margin:** $1,200 (80%)

---

### **Scenario C: 10 Customers, Business Tier**

**Revenue:** 10 × $99.99 \= $1,000/month  
 **Cost:** 10 × 1,000 × $0.03 \= $300/month  
 **Margin:** $700 (70%)

---

## **14\. Break-Even Analysis**

### **Fixed Costs (Monthly)**

* Infrastructure: $50  
* Domain/SSL: $10  
* Monitoring: $20  
* **Total Fixed:** $80/month

### **Variable Costs**

* Per scene: $0.03

**Break-even:** $80 / $0.03 \= **2,667 scenes**

At $0.15/scene pricing: **2,667 × $0.15 \= $400 revenue \= $320 profit**

**Break-even customers:** \~8-10 Starter tier users

---

## **15\. Risk Factors**

### **15.1 AI Model Price Changes**

**Risk:** AI provider increases pricing

**Mitigation:**

* Monitor provider pricing  
* Multi-provider strategy (Qwen, Wan, local models)  
* Build price increase buffer into margins

---

### **15.2 Compute Cost Spikes**

**Risk:** Unexpected GPU/CPU pricing changes

**Mitigation:**

* Lock in reserved instances  
* Hybrid CPU/GPU strategy  
* Batch processing optimizations

---

### **15.3 Storage Cost Growth**

**Risk:** Long-term storage accumulation

**Mitigation:**

* Aggressive cache expiration (7 days)  
* User-pays for persistent storage  
* Compress assets

---

## **16\. Cost Optimization Roadmap**

### **Phase 1 (v1.0)**

* ✅ CPU-based rendering  
* ✅ Basic layer graph caching  
* ✅ Timeouts and limits

### **Phase 2 (v1.5)**

* \[ \] Hybrid CPU/GPU rendering  
* \[ \] Advanced caching strategies  
* \[ \] Model usage optimization

### **Phase 3 (v2.0)**

* \[ \] Edge rendering (reduce bandwidth)  
* \[ \] Local model fallbacks  
* \[ \] Batch discount pricing

---

## **17\. CLI Commands**

### **Estimate Cost**

npm run cost:estimate \-- \\  
  \--scenes 6 \\  
  \--image-generation true \\  
  \--layer-extraction true

### **Cost Report**

npm run cost:report \-- \\  
  \--start-date 2026-01-01 \\  
  \--end-date 2026-01-31

---

## **18\. Summary**

**Per Scene Cost:** $0.02 \- $0.03  
 **Per Video (6 scenes):** $0.12 \- $0.18  
 **Target Margin:** 70-85%  
 **Break-Even:** \~10 customers  
 **Scalability:** Linear, no fixed costs

**Conclusion:** Economically viable at current pricing and cost structure.

---

## **19\. References**

* `architecture.md` \- System design affecting costs  
* `agent_contracts.md` \- AI agent cost drivers  
* `scene_library_v1.md` \- Rendering complexity

