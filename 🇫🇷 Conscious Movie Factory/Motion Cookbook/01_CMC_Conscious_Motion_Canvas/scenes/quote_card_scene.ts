import { makeScene2D } from '@motion-canvas/2d';
import { Rect, Txt, Layout, Line } from '@motion-canvas/2d/lib/components';
import { createRef, all } from '@motion-canvas/core';
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';
import { loadSceneConfig } from '../utils/config_loader';
import { applyBrandColors } from '../utils/brand_kit';

export default makeScene2D(function* (view) {
  const config = loadSceneConfig();
  const brand = applyBrandColors(config.brand_kit_id);
  const params = config.parameters;
  
  const quoteText = params.quote_text || "Your default quote here";
  const authorName = params.author_name || "";
  const showQuoteMarks = params.show_quote_marks !== false;
  
  // Refs
  const card = createRef<Rect>();
  const quote = createRef<Txt>();
  const underline = createRef<Line>();
  const author = createRef<Txt>();
  
  const displayQuote = showQuoteMarks ? `"${quoteText}"` : quoteText;
  
  view.add(
    <Rect
      ref={card}
      fill={brand.background}
      stroke={brand.primary}
      lineWidth={3}
      padding={50}
      radius={16}
      width={900}
      opacity={0}
      y={0}
    >
      <Layout
        direction="column"
        gap={30}
        alignItems="center"
      >
        {/* Quote text */}
        <Txt
          ref={quote}
          text={displayQuote}
          fontSize={32}
          fill={brand.text}
          fontFamily="Inter-Medium"
          textAlign="center"
          width={800}
          opacity={0}
        />
        
        {/* Decorative underline */}
        <Line
          ref={underline}
          points={[
            [-150, 0],
            [150, 0]
          ]}
          stroke={brand.primary}
          lineWidth={3}
          opacity={0}
          end={0}
        />
        
        {/* Author */}
        {authorName && (
          <Txt
            ref={author}
            text={`— ${authorName}`}
            fontSize={24}
            fill={brand.primary}
            fontFamily="Inter-Regular"
            fontStyle="italic"
            opacity={0}
          />
        )}
      </Layout>
    </Rect>
  );
  
  // Animation
  // Phase 1: Card fades in (0-18)
  yield* card().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 2: Quote appears (18-36)
  yield* quote().opacity(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 3: Underline draws (36-54)
  yield* underline().opacity(0, 0).to(1, 6, easeOutCubic);
  yield* underline().end(0, 0).to(1, 18, easeOutCubic);
  
  // Phase 4: Author fades in (54-72)
  if (authorName) {
    yield* author().opacity(0, 0).to(1, 18, easeOutCubic);
  }
  
  // Phase 5: Hold (72-150)
  yield* quote().opacity(1, 2.6);
});
