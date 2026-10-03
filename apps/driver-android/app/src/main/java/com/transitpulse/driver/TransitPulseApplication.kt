package com.transitpulse.driver

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build

class TransitPulseApplication : Application() {
    companion object {
        const val LOCATION_CHANNEL_ID = "location_service_channel"
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            const val channelName = "TransitPulse Location Tracking"
            val channel = NotificationChannel(
                LOCATION_CHANNEL_ID,
                channelName,
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Used to keep driver GPS tracking active in background"
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }
}
