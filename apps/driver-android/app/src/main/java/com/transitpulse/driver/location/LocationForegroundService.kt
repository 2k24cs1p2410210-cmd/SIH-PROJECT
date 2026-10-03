package com.transitpulse.driver.location

import android.app.Notification
import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.transitpulse.driver.R
import com.transitpulse.driver.TransitPulseApplication

class LocationForegroundService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification: Notification = NotificationCompat.Builder(this, TransitPulseApplication.LOCATION_CHANNEL_ID)
            .setContentTitle("TransitPulse Driver Active")
            .setContentText("Transmitting live bus GPS coordinates...")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .build()

        startForeground(1001, notification)
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
