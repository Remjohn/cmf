import { makeScene2D } from '@motion-canvas/2d';
import { Rect, Txt, Layout } from '@motion-canvas/2d/lib/components';
import { createRef } from '@motion-canvas/core';
import { easeOutCubic, linear } from '@motion-canvas/core/lib/tweening';
import { loadSceneConfig } from '../utils/config_loader';
import { applyBrandColors } from '../utils/brand_kit';

export default makeScene2D(function* (view) {
  // Load config
  const config = loadSceneConfig();
  const brand = applyBrandColors(config.brand_kit_id);
  const params = config.parameters;
  const timing = config.timing;
  
  // Extract parameters
  const finalValue = params.final_value || 7;
  const minValue = params.min_value || 0;
  const maxValue = params.max_value || 10;
  const labelText = params.label || "How confident do you feel?";
  
  // Create refs
  const label = createRef<Txt>();
  const barContainer = createRef<Rect>();
  const fillBar = createRef<Rect>();
  const valueText = createRef<Txt>();
  
  // Calculate dimensions
  const barWidth = 700;
  const barHeight = 50;
  const fillRatio = (finalValue - minValue) / (maxValue - minValue);
  const targetWidth = barWidth * fillRatio;
  
  // Determine timing
  let fillStartFrame = 30;
  let fillEndFrame = 90;
  let numberPopFrame = 102;
  
  if (timing.mode === "speech_aligned" && timing.anchors) {
    const anchors = timing.anchors;
    if (anchors.response_start && anchors.response_end) {
      fillStartFrame = anchors.response_start;
      fillEndFrame = anchors.response_end;
      numberPopFrame = fillEndFrame + 12;
    }
  }
  
  const fillDuration = fillEndFrame - fillStartFrame;
  
  // Build scene
  view.add(
    <Layout
      direction="column"
      gap={30}
      alignItems="center"
      y={-50}
    >
      {/* Question label */}
      <Txt
        ref={label}
        text={labelText}
        fontSize={26}
        fill={brand.text}
        fontFamily="Inter-Medium"
        opacity={0}
        textAlign="center"
        width={800}
      />
      
      {/* Bar container */}
      <Rect
        ref={barContainer}
        width={barWidth}
        height={barHeight}
        fill={brand.background}
        stroke="#3A3A3A"
        lineWidth={2}
        radius={8}
        opacity={0}
      >
        {/* Fill bar */}
        <Rect
          ref={fillBar}
          width={0}
          height={barHeight}
          fill={brand.primary}
          radius={8}
        />
      </Rect>
      
      {/* Value display */}
      <Txt
        ref={valueText}
        text={finalValue.toString()}
        fontSize={56}
        fill={brand.primary}
        fontFamily="SpaceGrotesk-Bold"
        opacity={0}
      />
    </Layout>
  );
  
  // Animation sequence
  // Phase 1: Setup (label and bar appear)
  yield* label().opacity(0, 0).to(1, 18, easeOutCubic);
  yield* barContainer().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Wait until speech start (if applicable)
  if (fillStartFrame > 48) {
    yield* fillBar().width(0, (fillStartFrame - 48) / 30);
  }
  
  // Phase 2: Progressive fill (aligned to speech)
  yield* fillBar().width(0, 0).to(targetWidth, fillDuration / 30, linear);
  
  // Phase 3: Lock and reveal number
  yield* valueText().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 4: Hold
  yield* fillBar().width(targetWidth, 0.5);
});
