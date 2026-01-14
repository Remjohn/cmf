# **quantitative\_component\_library.md**

**Purpose:** Numeric and data visualization components  
 **Status:** Canonical v1.0

---

## **1\. Purpose**

Quantitative components visualize numeric, ordinal, or progress information without making semantic assumptions. They are the visual building blocks for:

* Rating meters (1-10)  
* Progress bars  
* Before/after comparisons  
* Statistical displays  
* Response visualization (Goal.com-style)

---

## **2\. Design Principles**

1. **Display value, not meaning** \- Components show numbers/progress, not interpretation  
2. **Stateless rendering** \- No internal business logic  
3. **Motion token driven** \- Animation via METER\_FILL\_SMOOTH, NUMBER\_POP\_SOFT, etc.  
4. **Mobile-first** \- Legible at 1080×1920  
5. **Brand-neutral** \- Colors via brand kit injection

---

## **3\. Component Catalog**

### **3.1 HorizontalMeter**

**Purpose:** Linear scale for ratings (1-10, 0-100%)

**File:** `/src/components/quant/HorizontalMeter.tsx`

import { Rect, Layout, Txt } from '@motion-canvas/2d/lib/components';  
import { createRef } from '@motion-canvas/core';

export interface HorizontalMeterProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  minValue: number;  
  maxValue: number;  
  currentValue: number;  
  showTicks?: boolean;  
  showLabel?: boolean;  
  labelText?: string;  
  fillColor?: string;  
  backgroundColor?: string;  
}

export class HorizontalMeter extends Layout {  
  private fillBar \= createRef\<Rect\>();  
  private valueLabel \= createRef\<Txt\>();  
    
  constructor(props: HorizontalMeterProps) {  
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
      width: props.bbox.w \* 1080,  
      direction: 'column',  
      gap: 12,  
    });  
      
    // Label (optional)  
    if (props.showLabel && props.labelText) {  
      this.add(  
        \<Txt  
          text={props.labelText}  
          fontSize={24}  
          fill="\#CCCCCC"  
          fontFamily="Inter-Medium"  
        /\>  
      );  
    }  
      
    // Meter container  
    const meterHeight \= props.bbox.h \* 1920 \* 0.6;  
    this.add(  
      \<Rect  
        width="100%"  
        height={meterHeight}  
        fill={props.backgroundColor ?? '\#2A2A2A'}  
        radius={8}  
      \>  
        \<Rect  
          ref={this.fillBar}  
          width={0}  
          height="100%"  
          fill={props.fillColor ?? '\#00FFD1'}  
          radius={8}  
        /\>  
      \</Rect\>  
    );  
      
    // Value label  
    this.add(  
      \<Txt  
        ref={this.valueLabel}  
        text={props.currentValue.toString()}  
        fontSize={48}  
        fill="\#FFFFFF"  
        fontFamily="SpaceGrotesk-Bold"  
        opacity={0}  
      /\>  
    );  
  }  
    
  public \*animateTo(targetValue: number, duration: number) {  
    const { minValue, maxValue } \= this.props;  
    const fillRatio \= (targetValue \- minValue) / (maxValue \- minValue);  
    const targetWidth \= (this.props.bbox.w \* 1080\) \* fillRatio;  
      
    yield\* this.fillBar().width(0, 0).to(targetWidth, duration, easeOutCubic);  
      
    // Reveal number after fill completes  
    yield\* this.valueLabel().opacity(0, 0).to(1, 18, easeOutCubic);  
  }  
}

**Usage:**

\<HorizontalMeter  
  layerId="confidence\_meter"  
  bbox={{ x: 0.1, y: 0.5, w: 0.8, h: 0.15 }}  
  minValue={0}  
  maxValue={10}  
  currentValue={7}  
  showLabel={true}  
  labelText="Confidence Level"  
  fillColor="\#00FFD1"  
/\>

---

### **3.2 CircularDial**

**Purpose:** Radial meter for intensity, completion, confidence

**File:** `/src/components/quant/CircularDial.tsx`

import { Circle, Txt, Arc } from '@motion-canvas/2d/lib/components';  
import { createRef } from '@motion-canvas/core';

export interface CircularDialProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  minValue: number;  
  maxValue: number;  
  currentValue: number;  
  fillColor?: string;  
  strokeWidth?: number;  
}

export class CircularDial extends Layout {  
  private arc \= createRef\<Arc\>();  
  private centerLabel \= createRef\<Txt\>();  
    
  constructor(props: CircularDialProps) {  
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
    });  
      
    const radius \= (props.bbox.w \* 1080\) / 2;  
      
    // Background circle  
    this.add(  
      \<Circle  
        radius={radius}  
        stroke="\#2A2A2A"  
        lineWidth={props.strokeWidth ?? 12}  
      /\>  
    );  
      
    // Progress arc  
    this.add(  
      \<Arc  
        ref={this.arc}  
        radius={radius}  
        startAngle={-90}  
        endAngle={-90}  
        stroke={props.fillColor ?? '\#00FFD1'}  
        lineWidth={props.strokeWidth ?? 12}  
        lineCap="round"  
      /\>  
    );  
      
    // Center value  
    this.add(  
      \<Txt  
        ref={this.centerLabel}  
        text={props.currentValue.toString()}  
        fontSize={72}  
        fill="\#FFFFFF"  
        fontFamily="SpaceGrotesk-Bold"  
        opacity={0}  
      /\>  
    );  
  }  
    
  public \*animateTo(targetValue: number, duration: number) {  
    const { minValue, maxValue } \= this.props;  
    const fillRatio \= (targetValue \- minValue) / (maxValue \- minValue);  
    const targetAngle \= \-90 \+ (360 \* fillRatio);  
      
    yield\* this.arc().endAngle(-90, 0).to(targetAngle, duration, easeOutCubic);  
    yield\* this.centerLabel().opacity(0, 0).to(1, 18, easeOutCubic);  
  }  
}

---

### **3.3 BeforeAfterComparison**

**Purpose:** Side-by-side value comparison

**File:** `/src/components/quant/BeforeAfterComparison.tsx`

import { Layout, Rect, Txt } from '@motion-canvas/2d/lib/components';

export interface BeforeAfterProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  beforeValue: number;  
  afterValue: number;  
  minValue: number;  
  maxValue: number;  
  metricLabel?: string;  
}

export class BeforeAfterComparison extends Layout {  
  private beforeBar \= createRef\<Rect\>();  
  private afterBar \= createRef\<Rect\>();  
    
  constructor(props: BeforeAfterProps) {  
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
      width: props.bbox.w \* 1080,  
      direction: 'column',  
      gap: 24,  
    });  
      
    // Metric label  
    if (props.metricLabel) {  
      this.add(  
        \<Txt  
          text={props.metricLabel}  
          fontSize={28}  
          fill="\#CCCCCC"  
          fontFamily="Inter-Medium"  
        /\>  
      );  
    }  
      
    // Before meter  
    this.add(  
      \<Layout direction="row" gap={16} width="100%"\>  
        \<Txt text="Before" fontSize={24} fill="\#999999" width={100} /\>  
        \<Rect width="100%" height={40} fill="\#2A2A2A" radius={6}\>  
          \<Rect  
            ref={this.beforeBar}  
            width={0}  
            height="100%"  
            fill="\#777777"  
            radius={6}  
          /\>  
        \</Rect\>  
        \<Txt text={props.beforeValue.toString()} fontSize={32} fill="\#FFFFFF" /\>  
      \</Layout\>  
    );  
      
    // After meter  
    this.add(  
      \<Layout direction="row" gap={16} width="100%"\>  
        \<Txt text="After" fontSize={24} fill="\#999999" width={100} /\>  
        \<Rect width="100%" height={40} fill="\#2A2A2A" radius={6}\>  
          \<Rect  
            ref={this.afterBar}  
            width={0}  
            height="100%"  
            fill="\#00FFD1"  
            radius={6}  
          /\>  
        \</Rect\>  
        \<Txt text={props.afterValue.toString()} fontSize={32} fill="\#FFFFFF" /\>  
      \</Layout\>  
    );  
  }  
    
  public \*animateSequential(duration: number) {  
    const { minValue, maxValue, beforeValue, afterValue } \= this.props;  
    const containerWidth \= this.props.bbox.w \* 1080 \- 200; // Account for labels  
      
    const beforeRatio \= (beforeValue \- minValue) / (maxValue \- minValue);  
    const afterRatio \= (afterValue \- minValue) / (maxValue \- minValue);  
      
    // Animate before first  
    yield\* this.beforeBar().width(0, 0).to(  
      containerWidth \* beforeRatio,  
      duration,  
      easeOutCubic  
    );  
      
    // Then animate after  
    yield\* this.afterBar().width(0, 0).to(  
      containerWidth \* afterRatio,  
      duration,  
      easeOutCubic  
    );  
  }  
}

---

### **3.4 DeltaIndicator**

**Purpose:** Show improvement/decline magnitude

**File:** `/src/components/quant/DeltaIndicator.tsx`

import { Layout, Txt, Icon } from '@motion-canvas/2d/lib/components';

export interface DeltaIndicatorProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  deltaValue: number;  
  unit?: string;  
}

export class DeltaIndicator extends Layout {  
  constructor(props: DeltaIndicatorProps) {  
    const isPositive \= props.deltaValue \> 0;  
    const isNeutral \= props.deltaValue \=== 0;  
      
    const displayValue \= isPositive   
      ? \`+${props.deltaValue}${props.unit ?? ''}\`   
      : \`${props.deltaValue}${props.unit ?? ''}\`;  
      
    const color \= isNeutral ? '\#CCCCCC' : (isPositive ? '\#00FF88' : '\#FF4444');  
    const icon \= isNeutral ? null : (isPositive ? '↑' : '↓');  
      
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
      padding: 16,  
      fill: color \+ '22', // 22 \= 13% opacity  
      radius: 12,  
      direction: 'row',  
      gap: 12,  
      alignItems: 'center',  
      opacity: 0,  
    });  
      
    if (icon) {  
      this.add(  
        \<Txt  
          text={icon}  
          fontSize={36}  
          fill={color}  
          fontFamily="SpaceGrotesk-Bold"  
        /\>  
      );  
    }  
      
    this.add(  
      \<Txt  
        text={displayValue}  
        fontSize={48}  
        fill={color}  
        fontFamily="SpaceGrotesk-Bold"  
      /\>  
    );  
  }  
}

---

### **3.5 StackedValues**

**Purpose:** Vertical stack of multiple values (consensus)

**File:** `/src/components/quant/StackedValues.tsx`

import { Layout, Rect, Txt } from '@motion-canvas/2d/lib/components';

export interface StackedValuesProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  values: number\[\];  
  showAverage?: boolean;  
  highlightColor?: string;  
}

export class StackedValues extends Layout {  
  private valueElements: Txt\[\] \= \[\];  
  private averageElement \= createRef\<Txt\>();  
    
  constructor(props: StackedValuesProps) {  
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
      direction: 'column',  
      gap: 16,  
      alignItems: 'center',  
    });  
      
    // Individual values  
    props.values.forEach((value, index) \=\> {  
      const txtRef \= createRef\<Txt\>();  
      this.valueElements.push(txtRef);  
        
      this.add(  
        \<Rect  
          fill="\#2A2A2A"  
          padding={\[12, 24\]}  
          radius={8}  
          opacity={0}  
        \>  
          \<Txt  
            ref={txtRef}  
            text={value.toString()}  
            fontSize={36}  
            fill="\#FFFFFF"  
            fontFamily="SpaceGrotesk-Bold"  
          /\>  
        \</Rect\>  
      );  
    });  
      
    // Average (if enabled)  
    if (props.showAverage) {  
      const avg \= props.values.reduce((a, b) \=\> a \+ b, 0\) / props.values.length;  
        
      this.add(  
        \<Rect  
          fill={props.highlightColor ?? '\#00FFD1'}  
          padding={\[16, 32\]}  
          radius={12}  
          marginTop={24}  
          opacity={0}  
        \>  
          \<Layout direction="row" gap={12} alignItems="center"\>  
            \<Txt  
              text="Avg"  
              fontSize={24}  
              fill="\#000000"  
              fontFamily="Inter-Medium"  
            /\>  
            \<Txt  
              ref={this.averageElement}  
              text={avg.toFixed(1)}  
              fontSize={48}  
              fill="\#000000"  
              fontFamily="SpaceGrotesk-Bold"  
            /\>  
          \</Layout\>  
        \</Rect\>  
      );  
    }  
  }  
    
  public \*revealStaggered(staggerDelay: number) {  
    // Reveal values sequentially  
    for (const \[index, element\] of this.valueElements.entries()) {  
      yield\* element.parent().opacity(0, 0).to(1, 18, easeOutCubic);  
      if (index \< this.valueElements.length \- 1\) {  
        yield\* waitFor(staggerDelay);  
      }  
    }  
      
    // Reveal average  
    if (this.averageElement()) {  
      yield\* this.averageElement().parent().opacity(0, 0).to(1, 24, easeOutCubic);  
    }  
  }  
}

---

### **3.6 LowerThirdNumeric**

**Purpose:** Editorial numeric annotation

**File:** `/src/components/quant/LowerThirdNumeric.tsx`

import { Layout, Rect, Txt } from '@motion-canvas/2d/lib/components';

export interface LowerThirdNumericProps {  
  layerId: string;  
  bbox: { x: number; y: number; w: number; h: number };  
  value: number;  
  unit?: string;  
  contextLabel?: string;  
}

export class LowerThirdNumeric extends Layout {  
  constructor(props: LowerThirdNumericProps) {  
    super({  
      x: props.bbox.x \* 1080,  
      y: props.bbox.y \* 1920,  
      direction: 'column',  
      gap: 8,  
      opacity: 0,  
    });  
      
    // Context label  
    if (props.contextLabel) {  
      this.add(  
        \<Txt  
          text={props.contextLabel}  
          fontSize={20}  
          fill="\#999999"  
          fontFamily="Inter-Medium"  
          textTransform="uppercase"  
          letterSpacing={1}  
        /\>  
      );  
    }  
      
    // Value  
    this.add(  
      \<Txt  
        text={\`${props.value}${props.unit ?? ''}\`}  
        fontSize={56}  
        fill="\#FFFFFF"  
        fontFamily="SpaceGrotesk-Bold"  
      /\>  
    );  
  }  
}

---

## **4\. Common Patterns**

### **Pattern A: Single Value Reveal**

\<HorizontalMeter  
  layerId="rating"  
  bbox={{x: 0.1, y: 0.5, w: 0.8, h: 0.15}}  
  minValue={0}  
  maxValue={10}  
  currentValue={7}  
/\>

// Animate  
yield\* meter().animateTo(7, 30);

---

### **Pattern B: Before/After Transformation**

\<BeforeAfterComparison  
  layerId="progress"  
  bbox={{x: 0.1, y: 0.4, w: 0.8, h: 0.3}}  
  beforeValue={3}  
  afterValue={8}  
  minValue={0}  
  maxValue={10}  
  metricLabel="Confidence"  
/\>

yield\* comparison().animateSequential(30);

---

### **Pattern C: Delta Emphasis**

\<DeltaIndicator  
  layerId="improvement"  
  bbox={{x: 0.3, y: 0.3, w: 0.4, h: 0.1}}  
  deltaValue={+5}  
/\>

yield\* delta().opacity(0, 0).to(1, 18);

---

### **Pattern D: Consensus Stack**

\<StackedValues  
  layerId="consensus"  
  bbox={{x: 0.2, y: 0.3, w: 0.6, h: 0.5}}  
  values={\[7, 8, 6, 9, 7\]}  
  showAverage={true}  
/\>

yield\* stack().revealStaggered(0.2);

---

## **5\. Styling Constraints**

* **Minimum font size:** 20px (labels), 32px (values)  
* **Contrast ratio:** ≥ 4.5:1  
* **No gradients** inside quantitative components  
* **Border radius:** 4-12px max  
* **Stroke width:** 2-4px for outlines

---

## **6\. Motion Token Compatibility**

| Component | Compatible Tokens |
| ----- | ----- |
| HorizontalMeter | METER\_FILL\_SMOOTH, NUMBER\_POP\_SOFT |
| CircularDial | ARC\_DRAW, NUMBER\_POP\_SOFT |
| BeforeAfterComparison | METER\_FILL\_SMOOTH (sequential) |
| DeltaIndicator | DELTA\_POP\_UP, FADE\_IN |
| StackedValues | STACK\_REVEAL\_STAGGER, AVERAGE\_EMPHASIS |
| LowerThirdNumeric | LOWER\_THIRD\_SLIDE, NUMBER\_POP\_SOFT |

---

## **7\. Testing**

test('HorizontalMeter animates to correct width', async () \=\> {  
  const meter \= new HorizontalMeter({  
    layerId: 'test',  
    bbox: {x: 0, y: 0, w: 1, h: 0.1},  
    minValue: 0,  
    maxValue: 10,  
    currentValue: 7  
  });  
    
  await meter.animateTo(7, 30);  
    
  const fillRatio \= 7 / 10;  
  expect(meter.fillBar().width()).toBeCloseTo(1080 \* fillRatio);  
});

---

## **8\. Performance Notes**

* Components cache metric calculations  
* No per-frame recalculations  
* GPU-accelerated fills  
* Minimal garbage collection

---

## **9\. References**

* `motion_tokens.md` \- Animation primitives  
* `interview_scene_variants.md` \- Usage contexts  
* `speech_anchor_taxonomy.md` \- Timing coordination

