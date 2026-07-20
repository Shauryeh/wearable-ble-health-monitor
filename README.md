# Wearable BLE Health Monitor | Live Heart Rate & SpO₂ Dashboard

A full Bluetooth Low Energy (BLE) data pipeline that discovers a consumer wearable, inspects its GATT services, decodes notification packets, logs time-series health signals, and visualizes them in a live Streamlit dashboard.

## Why this project stands out

The wearable did not provide a public data API. I worked from raw BLE advertisements, services, characteristics, and notification payloads to build an end-to-end prototype around the device's heart-rate and oxygen-saturation signals.

**Core capabilities**

- Discovers nearby BLE devices and reports signal strength.
- Enumerates GATT services and characteristics for protocol inspection.
- Listens to candidate notification characteristics and prints raw hex packets.
- Extracts and validates heart-rate and SpO₂ fields from observed packet positions.
- Writes timestamped measurements and raw packets to CSV for reproducible analysis.
- Refreshes a live dashboard every two seconds with metrics, trends, and recent packets.

```mermaid
flowchart LR
    A["JCVital wearable"] -->|BLE notifications| B["Packet listener"]
    B --> C["Signal validation"]
    C --> D["CSV time series"]
    D --> E["Live Streamlit dashboard"]
```

## Technology

Python, Bleak, asyncio, Bluetooth Low Energy, pandas, Streamlit, time-series data processing

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Discover the wearable's address:

   ```bash
   python -m src.scan_band
   ```

4. Set the address in your shell. For example:

   ```bash
   export JCVITAL_BAND_ADDRESS="YOUR_DEVICE_ADDRESS"
   ```

5. Inspect services or listen to raw notifications when adapting the pipeline to a new device:

   ```bash
   python -m src.inspect_band
   python -m src.listen_band
   ```

6. Start the logger, then open the dashboard in a second terminal:

   ```bash
   python -m src.live_logger --minutes 30
   streamlit run dashboard.py
   ```

Runtime settings are documented in [`.env.example`](.env.example). Environment variables keep device-specific identifiers out of source control.

## Repository layout

```text
dashboard.py          Live Streamlit interface
src/scan_band.py      BLE device discovery
src/inspect_band.py   GATT service inspection
src/listen_band.py    Raw notification exploration
src/live_logger.py    Packet parsing and CSV logging
src/config.py         Environment-based configuration
```

## Engineering notes

- The packet offsets were inferred from repeated observations of this specific band and may differ across firmware or device models.
- Physiologic range checks reject implausible values before visualization while retaining the original packet for debugging.
- This is an engineering and research prototype, not a medical device. It must not be used for diagnosis or clinical decision-making.

## Future development

- Formal packet-schema validation across more recording sessions
- Automated reconnect and connection-health monitoring
- Local database storage and session comparisons
- Calibration against a reference pulse oximeter

## Author

Shauryeh Raj Kapur — Biomedical Engineering, healthcare AI, and connected-device development
