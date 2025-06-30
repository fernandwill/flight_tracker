# flight_tracker

![image](https://github.com/user-attachments/assets/664d840f-8e15-4da1-b134-57abc24dc554)

# ✈️ Flight Tracker

A simple Python-based flight tracking application that uses real-time data from the OpenSky Network API and visualizes it on an interactive world map using Bokeh.

## 🌐 Overview

This project retrieves live flight data, processes it with `pandas` and `numpy`, converts the coordinates to Web Mercator format, and plots the data using the Bokeh library with a tile map from CARTO.

The visualization includes:

* A global map of aircraft in the air
* Hover tooltips displaying:

  * Callsign
  * Origin Country
  * Velocity (m/s)
  * Altitude (m)

## 📁 Project Files

* `tracker.py` – The main script to fetch, process, and display flight data using Bokeh.
* `tracker.html` – A pre-generated HTML file to display the Bokeh map.

## 🔧 Requirements

Install the required Python packages:

```bash
pip install requests pandas numpy bokeh
```

## ▶️ How to Run

Run the tracker using Python:

```bash
python tracker.py
```

This will open an interactive map in your browser showing global aircraft positions in near real-time.

## 🧠 How It Works

1. Connects to the OpenSky API (`https://opensky-network.org/api/states/all`).
2. Retrieves flight data globally.
3. Filters and converts coordinates to Web Mercator.
4. Uses `Bokeh` to plot aircraft positions on a tile map.
5. Adds hover tooltips for each aircraft.

## 🗺️ Map Features

* Tile provider: `CARTODBPOSITRON` from Bokeh's vendor tiles
* Hoverable points representing aircraft
* Interactive zoom and pan

## 💡 Notes

* Data updates are based on a one-time fetch per run.
* OpenSky API may limit access during high traffic.

## 📸 Screenshot

*(Insert a screenshot of the generated map here)*

## 📜 License

This project is for educational and non-commercial purposes.

---

Let me know if you'd like the README styled differently (e.g., with emojis removed, or using markdown badges).


