# TransitPulse AI — ETA Strategy & Predictor Hierarchy

## 🔮 Fallback Predictor Hierarchy

TransitPulse AI uses a multi-tier predictor fallback mechanism to deliver robust ETAs even with zero historical dataset:

```
[ Incoming Request for Stop ETA ]
               │
               ▼
   [ 1. ML Model Predictor ] ──(Has >50 trained historical trip logs for route?)──► YES ──► Output XGBoost ETA
               │
              NO
               ▼
[ 2. Historical Avg Predictor ] ──(Has >10 completed segment traversals?)──► YES ──► Output Historical Segment Avg
               │
              NO
               ▼
[ 3. Current Speed Predictor ] ──(Is vehicle actively emitting GPS with valid speed?)──► YES ──► Output Distance / Speed
               │
              NO
               ▼
  [ 4. Schedule Fallback ] ────(Does timetable exist for route/stop?)───────────► YES ──► Output Timetable Schedule
               │
              NO
               ▼
  [ 5. Low-Confidence State ] ───► Return ETA: null, status: "Location unavailable"
```

---

## 📐 1. Predictor Definitions

### Tier 1: `MLModelPredictor` (XGBoost Trajectory Model)
* **Features**: Time of day, day of week, segment historical speed, weather/traffic indicator, current rolling speed, cumulative stop dwell time.
* **Activation Threshold**: Route must have $\ge 50$ fully completed trips in historical database.

### Tier 2: `HistoricalAveragePredictor`
* **Formula**:
  $$\text{ETA}_{\text{hist}} = \sum_{s \in S_{\text{remain}}} \bar{T}_{\text{segment}}(s) + N_{\text{stops}} \cdot \bar{D}_{\text{dwell}}$$
* **Activation Threshold**: Segment must have $\ge 10$ historical traversal samples.

### Tier 3: `CurrentSpeedPredictor` (Primary Bootstrapping Baseline)
* **Formula**:
  $$\text{ETA}_{\text{speed}} = \frac{d_{\text{remaining}}}{\max(v_{\text{current}}, v_{\text{min}})}$$
  Where $v_{\text{min}} = 2.0\text{ m/s}$ ($7.2\text{ km/h}$) and $v_{\text{max}} = 22.2\text{ m/s}$ ($80\text{ km/h}$).

### Tier 4: `ScheduleFallbackPredictor`
* Uses scheduled timetable time minus current clock time.

---

## 🛡️ 2. Confidence Scoring Algorithm

The `ConfidenceService` computes a continuous confidence score $C \in [0.0, 1.0]$:

$$C = w_1 \cdot C_{\text{freshness}} + w_2 \cdot C_{\text{accuracy}} + w_3 \cdot C_{\text{predictor}}$$

Where:
* $C_{\text{freshness}} = \max\left(0, 1.0 - \frac{\Delta t_{\text{last\_gps}}}{120\text{s}}\right)$
* $C_{\text{accuracy}} = \max\left(0, 1.0 - \frac{\text{accuracy\_m}}{50\text{m}}\right)$
* $C_{\text{predictor}}$:
  * `MLModel`: $0.95$
  * `HistoricalAverage`: $0.85$
  * `CurrentSpeed`: $0.70$
  * `ScheduleFallback`: $0.40$

### Confidence Levels & Ranges
* **High Confidence** ($C \ge 0.80$): Range $\pm 10\%$
* **Medium Confidence** ($0.50 \le C < 0.80$): Range $\pm 20\%$
* **Low Confidence** ($C < 0.50$): Range $\pm 40\%$
