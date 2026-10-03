package com.transitpulse.driver.location

import android.annotation.SuppressLint
import android.content.Context
import android.os.Looper
import com.google.android.gms.location.*

class LocationTracker(context: Context) {
    private val client: FusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(context)

    @SuppressLint("MissingPermission")
    fun startLocationUpdates(intervalMs: Long = 5000, onLocation: (android.location.Location) -> Unit) {
        val req = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, intervalMs)
            .setMinUpdateIntervalMillis(intervalMs / 2)
            .build()

        val callback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                result.lastLocation?.let { loc ->
                    if (LocationValidator.isValidLocation(loc)) {
                        onLocation(loc)
                    }
                }
            }
        }

        client.requestLocationUpdates(req, callback, Looper.getMainLooper())
    }
}
