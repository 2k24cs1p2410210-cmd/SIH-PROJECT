# TransitPulse AI — Driver Android App 🚌📱

Native Android application carried by bus drivers to act as active GPS beacons and transmit high-frequency location fixes every 5-10 seconds.

## Architecture & Components
- **Jetpack Compose**: Modern declarative UI.
- **Fused Location Provider**: High-precision Android Location API fix.
- **Foreground Location Service**: Persistent notification service preventing Android OS from killing location updates during background execution.
- **Room Database**: Local SQLite offline queue storing location fixes when network connectivity drops.
- **WorkManager (`SyncGpsWorker`)**: Background sync worker uploading cached location fixes when 3G/4G connectivity restores.
- **Retrofit 2**: Type-safe REST client uploading location updates to FastAPI backend.

## Permissions & Prerequisites
Requires the following Android permissions declared in `AndroidManifest.xml`:
- `ACCESS_FINE_LOCATION`
- `ACCESS_COARSE_LOCATION`
- `ACCESS_BACKGROUND_LOCATION` (Android 10+)
- `FOREGROUND_SERVICE` & `FOREGROUND_SERVICE_LOCATION` (Android 14+)
- `INTERNET` & `ACCESS_NETWORK_STATE`

## Build Instructions
1. Open `apps/driver-android` in Android Studio (Jellyfish / Koala or newer).
2. Sync Gradle files (`./gradlew build`).
3. Set Backend API URL in `RetrofitClient.kt` (e.g. `http://10.0.2.2:8000` for Android Emulator or your local IP for physical device).
4. Deploy to Android device / emulator (minSDK 26, targetSDK 34).
