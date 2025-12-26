# AI Image Generator 🎨🤖

A web-based AI Image Generator that transforms text prompts into images using **Stable Diffusion**.
The project demonstrates **real-world deployment architecture** by separating frontend delivery and AI inference for stability and performance.

---

## 🔗 Live Links

* **Frontend (UI – Vercel):**
  👉 [https://ai-image-generator-fawn-three.vercel.app/](https://ai-image-generator-fawn-three.vercel.app/)

* **AI Inference Demo (Hugging Face Spaces):**
  👉 [https://pranith0410-ai-image-generator.hf.space](https://pranith0410-ai-image-generator.hf.space)

---

## 🧠 Project Overview

This project allows users to generate images from text prompts using **Stable Diffusion**.

Due to the **long-running and compute-intensive nature of AI image generation**, the application is designed with a **decoupled architecture**:

* The **frontend UI** is deployed on **Vercel** for fast, global access.
* The **AI inference backend** is hosted on **Hugging Face Spaces**, which is optimized for ML workloads.

This design ensures **stability, reliability, and scalability**.

---

## 🏗️ Architecture

```
User
 ↓
Frontend UI (Vercel)
 ↓
Hugging Face Spaces (Stable Diffusion Inference)
 ↓
Generated Image
```

> The frontend opens the Hugging Face inference demo in a new tab instead of directly calling the backend API.
> This avoids unreliable browser-based calls for long-running ML tasks.

---

## 🚀 Features

* Text-to-image generation using **Stable Diffusion**
* Clean and responsive frontend UI
* Deployed frontend on **Vercel**
* Deployed AI inference on **Hugging Face Spaces**
* CPU-optimized inference for free-tier environments
* Production-aware system design

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Vercel (Deployment)

### Backend / AI

* Python
* Stable Diffusion (Diffusers)
* Gradio
* Hugging Face Spaces

---

## 📌 Why the Output Is Generated on Hugging Face

AI image generation:

* Is **compute-intensive**
* Can take **30–120 seconds** on CPU
* Uses **queue-based execution**

Hugging Face Spaces are designed for:

* Handling ML queues
* Managing model state
* Providing reliable inference UIs

Attempting to force this inference through browser `fetch()` calls can lead to:

* Timeouts
* CORS issues
* Unstable behavior

👉 Therefore, the frontend cleanly redirects users to the inference demo.

This is a **deliberate and professional design decision**, not a limitation.

---

## 📂 Repository Structure

```
AI-image-generator/
├── index.html
└── README.md
```

---

## 📈 Future Improvements

* Host a dedicated backend API using FastAPI / Render
* Add GPU-based inference for faster generation
* Enable prompt history and image downloads
* Integrate Hugging Face Inference API with authentication

---

## 👤 Author

**Pranith Goud**
B.Tech Student | AI & ML Enthusiast

---

## 📜 License

This project is licensed under the MIT License.

---
