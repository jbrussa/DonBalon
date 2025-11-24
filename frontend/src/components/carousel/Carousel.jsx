import React, { useEffect, useState, useRef } from "react";
import "./Carousel.css";

// Simple, dependency-free carousel that loads images from public/photos
// Usage: <Carousel folder="/photos" interval={4000} />

export default function Carousel({ folder = "/photos", interval = 4000 }) {
  const [images, setImages] = useState([]);
  const [index, setIndex] = useState(0);
  const timer = useRef(null);

  useEffect(() => {
    // Try to discover images by fetching an index.json if present; otherwise infer common names.
    // We'll attempt to load photos/photo1.jpg..photo8.jpg until a 404.
    async function discover() {
      const found = [];
      // Try index.json first
      try {
        const r = await fetch(`${folder}/index.json`);
        if (r.ok) {
          const list = await r.json();
          if (Array.isArray(list)) {
            setImages(list.map((p) => encodeURI(`${folder}/${p}`)));
            return;
          }
        }
      } catch (e) {
        // ignore
      }

      // Fallback: try common names and extensions (jpg/png/webp)
      const exts = ["jpg", "png", "webp"];
      const candidates = [];
      for (const ext of exts) {
        for (let i = 1; i <= 12; i++) {
          candidates.push(`${folder}/photo${i}.${ext}`);
        }
      }
      // Also try common 'unnamed' patterns (the files in your screenshot use these names)
      const unnamedCandidates = [
        "unnamed.webp",
        "unnamed (1).webp",
        "unnamed (2).webp",
        "unnamed (3).webp",
        "unnamed (4).webp",
        "unnamed.png",
        "unnamed.jpg",
      ];
      for (const name of unnamedCandidates)
        candidates.push(`${folder}/${name}`);

      // Try loading images via Image() (more reliable than HEAD for static files)
      function tryLoad(src) {
        return new Promise((resolve) => {
          const img = new Image();
          const encoded = encodeURI(src);
          img.onload = () => resolve(encoded);
          img.onerror = () => resolve(null);
          img.src = encoded;
        });
      }

      const loadResults = await Promise.all(candidates.map((c) => tryLoad(c)));
      for (const r of loadResults) {
        if (r && !found.includes(r)) found.push(r);
      }

      setImages(found);
    }

    discover();
  }, [folder]);

  useEffect(() => {
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = null;
    }
    if (images.length <= 1) return;
    // start rotation
    timer.current = setInterval(
      () => setIndex((i) => (i + 1) % images.length),
      interval
    );
    return () => {
      if (timer.current) {
        clearInterval(timer.current);
        timer.current = null;
      }
    };
  }, [images, interval]);

  // Debug: log images and index changes
  useEffect(() => {
    console.debug("Carousel images:", images);
  }, [images]);

  useEffect(() => {
    console.debug("Carousel index:", index);
  }, [index]);

  function go(n) {
    setIndex(((n % images.length) + images.length) % images.length);
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = setInterval(
        () => setIndex((i) => (i + 1) % images.length),
        interval
      );
    }
  }

  if (!images || images.length === 0) {
    return (
      <div className="carousel-placeholder">
        <div>No se encontraron imágenes en {folder}</div>
      </div>
    );
  }

  return (
    <div className="carousel-root">
      <div className="carousel-inner">
        {images.map((src, i) => (
          <div
            key={src}
            className={`carousel-item ${i === index ? "active" : ""}`}
            style={{ backgroundImage: `url(${src})` }}
            aria-hidden={i !== index}
          />
        ))}

        <button
          className="carousel-nav prev"
          onClick={() => go(index - 1)}
          aria-label="Anterior"
        >
          ‹
        </button>
        <button
          className="carousel-nav next"
          onClick={() => go(index + 1)}
          aria-label="Siguiente"
        >
          ›
        </button>

        <div className="carousel-dots">
          {images.map((_, i) => (
            <button
              key={i}
              className={`dot ${i === index ? "active" : ""}`}
              onClick={() => go(i)}
              aria-label={`Ir a ${i + 1}`}
            ></button>
          ))}
        </div>

        {/* Debug thumbnails to help diagnose duplicate/ordering issues */}
        <div
          style={{
            display: "flex",
            gap: 8,
            justifyContent: "center",
            paddingTop: 10,
          }}
        >
          {images.map((s, i) => (
            <img
              key={`${s}-${i}`}
              src={s}
              alt={`thumb-${i}`}
              style={{
                width: 80,
                height: 48,
                objectFit: "cover",
                border:
                  i === index
                    ? "3px solid #18a16b"
                    : "1px solid rgba(0,0,0,0.08)",
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
