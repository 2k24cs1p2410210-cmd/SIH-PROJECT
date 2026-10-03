package com.transitpulse.driver.data.repository

import com.transitpulse.driver.data.remote.RetrofitClient
import com.transitpulse.driver.data.remote.StartTripApiRequest

class TripRepository {
    suspend fun startTrip(busId: String, routeId: String): String? {
        return try {
            val resp = RetrofitClient.api.startTrip(StartTripApiRequest(busId, routeId))
            if (resp.isSuccessful) resp.body()?.trip_id else null
        } catch (e: Exception) {
            "trip-demo-01" // Fallback local offline demo trip ID
        }
    }

    suspend fun endTrip(tripId: String): Boolean {
        return try {
            val resp = RetrofitClient.api.endTrip(tripId)
            resp.isSuccessful
        } catch (e: Exception) {
            true
        }
    }
}
