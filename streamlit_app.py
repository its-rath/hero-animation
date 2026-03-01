import streamlit as st

st.set_page_config(
    page_title="Scroll Car Animation | Hero Section",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stAppHeader { display: none; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        iframe { border: none !important; }
        footer { display: none; }
        #MainMenu { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Scroll Car Animation</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #121212;
    color: #fff;
    font-family: Arial, sans-serif;
    overflow-x: hidden;
  }
  html { scroll-behavior: smooth; }

  .hero-section { position: relative; height: 300vh; background: #121212; }

  .track {
    display: flex;
    height: 100vh;
    width: 100%;
    align-items: center;
    justify-content: center;
    background: #d1d1d1;
    position: relative;
  }

  .road {
    position: relative;
    width: 100%;
    height: 200px;
    background: #1e1e1e;
    overflow: hidden;
  }

  .car {
    position: absolute;
    left: 0;
    top: 0;
    height: 200px;
    z-index: 10;
  }
  .car img {
    height: 100%;
    width: auto;
    object-fit: contain;
  }

  .trail {
    position: absolute;
    left: 0;
    top: 0;
    height: 200px;
    width: 0;
    background: #45db7d;
    z-index: 1;
  }

  .headline {
    position: absolute;
    z-index: 5;
    display: flex;
    gap: 2px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: clamp(3rem, 8vw, 8rem);
    font-weight: 700;
  }
  .headline span {
    opacity: 0;
    color: #111;
    transition: opacity 0.1s;
  }

  .stat-box {
    position: absolute;
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: 4px;
    border-radius: 12px;
    padding: 24px 28px;
    opacity: 0;
    transform: translateY(20px);
  }
  .stat-box .pct {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
  }
  .stat-box .desc { font-size: 1rem; }
</style>
</head>
<body>

<section class="hero-section" id="heroSection">
  <div class="track" id="track">
    <div class="road" id="road">
      <div class="car" id="car">
        <img src="https://paraschaturvedi.github.io/car-scroll-animation/McLaren%20720S%202022%20top%20view.png" alt="McLaren 720S" />
      </div>
      <div class="trail" id="trail"></div>
      <div class="headline" id="headline"></div>
    </div>

    <div class="stat-box" id="box1" style="top:5%; right:30%; background:#def54f; color:#111;">
      <span class="pct">58%</span>
      <span class="desc">Increase in pick up point use</span>
    </div>
    <div class="stat-box" id="box2" style="bottom:5%; right:35%; background:#6ac9ff; color:#111;">
      <span class="pct">23%</span>
      <span class="desc">Decreased in customer phone calls</span>
    </div>
    <div class="stat-box" id="box3" style="top:5%; right:10%; background:#333; color:#fff;">
      <span class="pct">27%</span>
      <span class="desc">Increase in pick up point use</span>
    </div>
    <div class="stat-box" id="box4" style="bottom:5%; right:12.5%; background:#fa7328; color:#111;">
      <span class="pct">40%</span>
      <span class="desc">Decreased in customer phone calls</span>
    </div>
  </div>
</section>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
  gsap.registerPlugin(ScrollTrigger);

  const letters = "WELCOME ITZFIZZ".split("");
  const headlineEl = document.getElementById("headline");
  letters.forEach((ch) => {
    const span = document.createElement("span");
    span.textContent = ch === " " ? "\\u00A0" : ch;
    headlineEl.appendChild(span);
  });

  const section = document.getElementById("heroSection");
  const track = document.getElementById("track");
  const car = document.getElementById("car");
  const trail = document.getElementById("trail");
  const road = document.getElementById("road");
  const spans = headlineEl.querySelectorAll("span");

  const roadWidth = road.offsetWidth;
  const carWidth = car.offsetWidth;
  const endX = roadWidth;

  const roadLeft = road.getBoundingClientRect().left;
  const letterPositions = Array.from(spans).map(
    (l) => l.getBoundingClientRect().left - roadLeft + l.offsetWidth / 2
  );

  ScrollTrigger.create({
    trigger: section,
    start: "top top",
    end: "bottom bottom",
    pin: track,
    scrub: 1,
  });

  gsap.to(car, {
    x: endX,
    ease: "none",
    scrollTrigger: {
      trigger: section,
      start: "top top",
      end: "bottom bottom",
      scrub: 1,
      onUpdate: function (self) {
        const currentX = self.progress * endX;
        trail.style.width = currentX + "px";

        spans.forEach(function (span, i) {
          const letterX = letterPositions[i] || 0;
          span.style.opacity = (currentX + carWidth / 2) >= letterX ? "1" : "0";
        });
      },
    },
  });

  const scrollPoints = [0.15, 0.3, 0.45, 0.55];
  const boxes = ["box1", "box2", "box3", "box4"];
  boxes.forEach(function (id, i) {
    const el = document.getElementById(id);
    if (!el) return;
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.5,
      scrollTrigger: {
        trigger: section,
        start: "top+=" + (scrollPoints[i] * 100) + "% top",
        end: "top+=" + ((scrollPoints[i] + 0.1) * 100) + "% top",
        scrub: 1,
      },
    });
  });
</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=2800, scrolling=True)
