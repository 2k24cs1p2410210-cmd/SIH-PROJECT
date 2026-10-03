package com.transitpulse.driver.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "gps_queue")
data class GpsPointEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val tripId: String,
    val busId: String,
    val latitude: Double,
    val longitude: Double,
    val speedMps: Float,
    val heading: Float,
    val accuracyM: Float,
    val recordedAtEpoch: Long,
    val isSynced: Boolean = false
)
