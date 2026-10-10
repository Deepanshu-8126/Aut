import React from 'react';
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface CameraKey {
  t: number;      // seconds, scene start se
  zoom?: number;  // 1 = normal, 1.4 = thoda zoom, 1.8 = bada zoom
  x?: number;     // zoom center, % (0-100) horizontal
  y?: number;     // zoom center, % (0-100) vertical
}

// Scene visual ko smooth zoom in/out karta hai. Keyframes ke beech ease-in-out.
export const Camera: React.FC<{ keys?: CameraKey[]; children: React.ReactNode }> = ({ keys, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!keys || keys.length === 0) return <>{children}</>;

  const ks = [...keys].sort((a, b) => a.t - b.t).map((k) => ({
    t: k.t, zoom: k.zoom ?? 1, x: k.x ?? 50, y: k.y ?? 50,
  }));
  const time = frame / fps;

  let zoom = ks[0].zoom, x = ks[0].x, y = ks[0].y;
  if (time >= ks[ks.length - 1].t) {
    const last = ks[ks.length - 1];
    zoom = last.zoom; x = last.x; y = last.y;
  } else {
    for (let i = 0; i < ks.length - 1; i++) {
      const a = ks[i], b = ks[i + 1];
      if (time >= a.t && time < b.t) {
        const ease = Easing.inOut(Easing.cubic);
        zoom = interpolate(time, [a.t, b.t], [a.zoom, b.zoom], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        x = interpolate(time, [a.t, b.t], [a.x, b.x], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        y = interpolate(time, [a.t, b.t], [a.y, b.y], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        break;
      }
    }
  }
  return (
    <div style={{ width: '100%', height: '100%', transform: `scale(${zoom})`, transformOrigin: `${x}% ${y}%` }}>
      {children}
    </div>
  );
};
