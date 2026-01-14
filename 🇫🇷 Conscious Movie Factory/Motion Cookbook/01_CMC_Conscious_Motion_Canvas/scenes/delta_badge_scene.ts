import { makeScene2D } from '@motion-canvas/2d';
import { Rect, Txt, Layout } from '@motion-canvas/2d/lib/components';
import { createRef, all } from '@motion-canvas/core';
import { easeOutCubic, easeOutBack } from '@motion-canvas/core/lib/tweening';
import { loadSceneConfig } from '../utils/config_loader';
import { applyBrandColors } from '../utils/brand_kit';

export default makeScene2D(function* (view) {
  const config = loadSceneConfig();
  const brand = applyBrandColors(config.brand_kit_id);
  const params = config.parameters;
  
  const startValue = params.start_value || 3;
  const endValue = params.end_value || 7;
  const deltaValue = endValue - startValue;
  const unit = params.delta_unit || "points";
  
  // Refs
  const oldValueText = createRef<Txt>();
  const arrow = createRef<Txt>();
  const newValueText = createRef<Txt>();
  const deltaBadge = createRef<Rect>();
  const deltaText = createRef<Txt>();
  
  // Color based on positive/negative
  const isPositive = deltaValue > 0;
  const deltaColor = isPositive ? "#00FF88" : "#FF4444";
  const deltaSign = isPositive ? "+" : "";
  
  view.add(
    <Layout
      direction="column"
      gap={40}
      alignItems="center"
      y={-30}
    >
      {/* Old → New transition */}
      <Layout direction="row" gap={30} alignItems="center">
        <Txt
          ref={oldValueText}
          text={startValue.toString()}
          fontSize={64}
          fill="#666666"
          fontFamily="SpaceGrotesk-Bold"
          opacity={0}
        />
        
        <Txt
          ref={arrow}
          text="→"
          fontSize={48}
          fill="#888888"
          opacity={0}
        />
        
        <Txt
          ref={newValueText}
          text={endValue.toString()}
          fontSize={64}
          fill={brand.primary}
          fontFamily="SpaceGrotesk-Bold"
          opacity={0}
        />
      </Layout>
      
      {/* Delta badge */}
      <Rect
        ref={deltaBadge}
        fill={deltaColor + "22"}
        stroke={deltaColor}
        lineWidth={3}
        padding={[16, 32]}
        radius={16}
        opacity={0}
        scale={0.8}
      >
        <Txt
          ref={deltaText}
          text={`${deltaSign}${deltaValue} ${unit}`}
          fontSize={48}
          fill={deltaColor}
          fontFamily="SpaceGrotesk-Bold"
        />
      </Rect>
    </Layout>
  );
  
  // Animation
  // Phase 1: Old value (0-30)
  yield* oldValueText().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 2: Arrow (30-42)
  yield* arrow().opacity(0, 0).to(1, 12, easeOutCubic);
  
  // Phase 3: New value (42-60)
  yield* newValueText().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 4: Delta badge pops (60-78)
  yield* all(
    deltaBadge().opacity(0, 0).to(1, 18, easeOutCubic),
    deltaBadge().scale(0.8, 0).to(1.0, 18, easeOutBack)
  );
  
  // Phase 5: Hold (78-120)
  yield* deltaBadge().scale(1.0, 1.4);
});
