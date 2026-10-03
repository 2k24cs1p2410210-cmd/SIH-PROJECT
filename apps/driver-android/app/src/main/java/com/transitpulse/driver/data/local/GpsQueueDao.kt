package com.transitpulse.driver.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

@Dao
interface GpsQueueDao {
    @Insert
    suspend fun insertPoint(point: GpsPointEntity): Long

    @Query("SELECT * FROM gps_queue WHERE isSynced = 0 ORDER BY recordedAtEpoch ASC LIMIT 50")
    suspend fun getUnsyncedPoints(): List<GpsPointEntity>

    @Query("DELETE FROM gps_queue WHERE id IN (:ids)")
    suspend fun deleteSyncedPoints(ids: List<Long>)

    @Query("SELECT COUNT(*) FROM gps_queue WHERE isSynced = 0")
    suspend fun getQueuedCount(): Int
}
