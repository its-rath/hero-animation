"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const HEADLINE_LETTERS = [
  "W", "E", "L", "C", "O", "M", "E", "\u00A0", "I", "T", "Z", "F", "I", "Z", "Z",
];

const STATS = [
  {
    id: "box1", pct: "58%", desc: "Increase in pick up point use",
    bg: "#def54f", color: "#111", pos: { top: "5%", right: "30%" }
  },
  {
    id: "box2", pct: "23%", desc: "Decreased in customer phone calls",
    bg: "#6ac9ff", color: "#111", pos: { bottom: "5%", right: "35%" }
  },
  {
    id: "box3", pct: "27%", desc: "Increase in pick up point use",
    bg: "#333", color: "#fff", pos: { top: "5%", right: "10%" }
  },
  {
    id: "box4", pct: "40%", desc: "Decreased in customer phone calls",
    bg: "#fa7328", color: "#111", pos: { bottom: "5%", right: "12.5%" }
  },
];

export default function Home() {
  const sectionRef = useRef(null);
  const trackRef = useRef(null);
  const carRef = useRef(null);
  const trailRef = useRef(null);
  const lettersRef = useRef([]);
  const roadRef = useRef(null);

  useEffect(() => {
    if (!carRef.current || !sectionRef.current || !trackRef.current) return;

    const roadWidth = roadRef.current?.offsetWidth || window.innerWidth;
    const carWidth = carRef.current.offsetWidth;
    const endX = roadWidth - carWidth;

    const roadLeft = roadRef.current?.getBoundingClientRect().left || 0;
    const letterPositions = lettersRef.current.map((l) =>
      l ? l.getBoundingClientRect().left - roadLeft + l.offsetWidth / 2 : 0
    );

    ScrollTrigger.create({
      trigger: sectionRef.current,
      start: "top top",
      end: "bottom bottom",
      pin: trackRef.current,
      scrub: 1,
    });

    const carTween = gsap.to(carRef.current, {
      x: endX,
      ease: "none",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top top",
        end: "bottom bottom",
        scrub: 1,
        onUpdate: (self) => {
          const currentX = self.progress * endX;

          if (trailRef.current) {
            gsap.set(trailRef.current, { width: currentX + carWidth / 2 });
          }

          lettersRef.current.forEach((letter, i) => {
            if (!letter) return;
            const letterX = letterPositions[i] || 0;
            letter.style.opacity = (currentX + carWidth / 2) >= letterX ? "1" : "0";
          });
        },
      },
    });

    const scrollPoints = [0.15, 0.3, 0.45, 0.55];
    const statTweens = STATS.map((stat, i) => {
      const el = document.getElementById(stat.id);
      if (!el) return null;
      return gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 0.5,
        scrollTrigger: {
          trigger: sectionRef.current,
          start: `top+=${scrollPoints[i] * 100}% top`,
          end: `top+=${(scrollPoints[i] + 0.1) * 100}% top`,
          scrub: 1,
        },
      });
    });

    return () => {
      ScrollTrigger.getAll().forEach((t) => t.kill());
      carTween?.kill();
      statTweens.forEach((t) => t?.kill());
    };
  }, []);

  return (
    <>
      <section ref={sectionRef} className="relative bg-[#121212]"
        style={{ height: "300vh" }}>

        <div ref={trackRef}
          className="flex h-screen w-full items-center justify-center bg-[#d1d1d1]"
          style={{ position: "relative" }}>

          <div ref={roadRef}
            className="relative w-full overflow-hidden bg-[#1e1e1e]"
            style={{ height: "200px" }}>

            <div ref={carRef}
              className="absolute left-0 top-0 z-10"
              style={{ height: "200px" }}>
              <img
                src="/car.png"
                alt="McLaren 720S top view"
                className="h-full w-auto object-contain"
              />
            </div>

            <div ref={trailRef}
              className="absolute left-0 top-0 z-[1] bg-[#45db7d]"
              style={{ height: "200px", width: 0 }}
            />

            <div className="absolute z-[5] flex gap-1"
              style={{ top: "50%", left: "50%", transform: "translate(-50%, -50%)", fontSize: "clamp(3rem, 8vw, 8rem)", fontWeight: 700 }}>
              {HEADLINE_LETTERS.map((letter, i) => (
                <span key={i}
                  ref={(el) => (lettersRef.current[i] = el)}
                  style={{ opacity: 0, color: "#111", transition: "opacity 0.1s" }}>
                  {letter}
                </span>
              ))}
            </div>
          </div>

          {STATS.map((stat) => (
            <div key={stat.id} id={stat.id}
              className="absolute z-[5] flex flex-col items-start justify-center gap-1 rounded-xl"
              style={{
                ...stat.pos,
                backgroundColor: stat.bg,
                color: stat.color,
                padding: "24px 28px",
                opacity: 0,
                transform: "translateY(20px)",
              }}>
              <span className="text-5xl font-bold leading-none">
                {stat.pct}
              </span>
              <span className="text-base">{stat.desc}</span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
