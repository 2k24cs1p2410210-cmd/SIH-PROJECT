package com.transitpulse.driver.data.repository

import android.content.Context
import com.transitpulse.driver.data.local.AppDatabase
import com.transitpulse.driver.data.local.GpsPointEntity
import com.transitpulse.driver.data.remote.GpsUpdatePayload
import com.transitpulse.driver.data.remote.RetrofitClient

class LocationRepository(context: Context) {
    private val db = AppDatabase.getInstance(context)
    private val dao = db.gpsQueueDao()

    suspend fun recordAndSendLocation(payload: GpsUpdatePayload): Boolean {
        return try {
            val resp = RetrofitClient.api.sendGpsUpdate(payload)
            if (resp.isSuccessful && resp.body()?.status == "success") {
                true
            } else {
                // Queue locally if network upload failed
                saveToOfflineQueue(payload)
                false
            }
        } catch (e: Exception) {
            // Queue locally on exception
            saveToOfflineQueue(payload)
            false
        }
    }

    private suspend fun saveToOfflineQueue(payload: GpsUpdatePayload) {
        val entity = GpsPointEntity(
            tripId = payload.trip_id,
            busId = payload.bus_id,
            latitude = payload.latitude,
            longitude = payload.longitude,
            speedMps = payload.speed_mps,
            heading = payload.heading,
            accuracyM = payload.accuracy_m,
            recordedAtEpoch = System.currentTimeMillis()
        )
        dao.insertPoint(entity)
    }

    suspend fun getQueuedPointCount(): Int {
        return dao.getQueuedCount()
    }
}
