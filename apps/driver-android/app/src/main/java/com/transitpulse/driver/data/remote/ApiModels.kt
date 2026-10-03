package com.transitpulse.driver.data.remote

data class GpsUpdatePayload(
    val trip_id: String,
    val bus_id: String,
    val latitude: Double,
    val longitude: Double,
    val altitude: Double? = null,
    val speed_mps: Float,
    val heading: Float,
    val accuracy_m: Float,
    val recorded_at: String,
    val battery_level: Int? = null
)

data class GpsUpdateApiResponse(
    val status: String,
    val point_id: Long?,
    val is_processed: Boolean,
    val route_distance_m: Double?,
    val eta_updated: Boolean
)

data class StartTripApiRequest(
    val bus_id: String,
    val route_id: String,
    val driver_id: String? = null
)

data class TripApiResponse(
    val trip_id: String,
    val bus_id: String,
    val route_id: String,
    val status: String,
    val start_time: String,
    val end_time: String? = null
)
