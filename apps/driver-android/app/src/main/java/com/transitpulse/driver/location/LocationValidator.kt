package com.transitpulse.driver.location

import android.location.Location

object LocationValidator {
    private const val MAX_ACCURACY_THRESHOLD_M = 50.0f

    fun isValidLocation(location: Location): Boolean {
        if (!location.hasAccuracy()) return false
        if (location.accuracy > MAX_ACCURACY_THRESHOLD_M) return false
        if (location.latitude !in -90.0..90.0) return false
        if (location.longitude !in -180.0..180.0) return false
        return true
    }
}
