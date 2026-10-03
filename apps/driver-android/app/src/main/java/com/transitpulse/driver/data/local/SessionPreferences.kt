package com.transitpulse.driver.data.local

import android.content.Context
import android.content.SharedPreferences

class SessionPreferences(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("driver_session_prefs", Context.MODE_PRIVATE)

    var activeTripId: String?
        get() = prefs.getString("active_trip_id", null)
        set(value) = prefs.edit().putString("active_trip_id", value).apply()

    var assignedBusId: String?
        get() = prefs.getString("assigned_bus_id", "bus-101")
        set(value) = prefs.edit().putString("assigned_bus_id", value).apply()

    var activeRouteId: String?
        get() = prefs.getString("active_route_id", "route-001")
        set(value) = prefs.edit().putString("active_route_id", value).apply()

    var authToken: String?
        get() = prefs.getString("auth_token", null)
        set(value) = prefs.edit().putString("auth_token", value).apply()
}
