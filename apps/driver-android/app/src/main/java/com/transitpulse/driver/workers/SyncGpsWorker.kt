package com.transitpulse.driver.workers

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.transitpulse.driver.data.local.AppDatabase
import com.transitpulse.driver.data.remote.GpsUpdatePayload
import com.transitpulse.driver.data.remote.RetrofitClient

class SyncGpsWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val db = AppDatabase.getInstance(applicationContext)
        val dao = db.gpsQueueDao()

        val unsyncedPoints = dao.getUnsyncedPoints()
        if (unsyncedPoints.isEmpty()) return Result.success()

        val syncedIds = mutableListOf<Long>()

        for (pt in unsyncedPoints) {
            val payload = GpsUpdatePayload(
                trip_id = pt.tripId,
                bus_id = pt.busId,
                latitude = pt.latitude,
                longitude = pt.longitude,
                speed_mps = pt.speedMps,
                heading = pt.heading,
                accuracy_m = pt.accuracyM,
                recorded_at = java.time.Instant.ofEpochMilli(pt.recordedAtEpoch).toString()
            )

            try {
                val resp = RetrofitClient.api.sendGpsUpdate(payload)
                if (resp.isSuccessful) syncedIds.add(pt.id)
            } catch (e: Exception) {
                // Break and retry later
                break
            }
        }

        if (syncedIds.isNotEmpty()) {
            dao.deleteSyncedPoints(syncedIds)
        }

        return Result.success()
    }
}
