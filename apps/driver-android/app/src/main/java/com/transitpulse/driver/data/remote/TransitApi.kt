package com.transitpulse.driver.data.remote

import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.Query

interface TransitApi {
    @POST("api/v1/gps/update")
    suspend fun sendGpsUpdate(@Body payload: GpsUpdatePayload): Response<GpsUpdateApiResponse>

    @POST("api/v1/trips/start")
    suspend fun startTrip(@Body payload: StartTripApiRequest): Response<TripApiResponse>

    @POST("api/v1/trips/end")
    suspend fun endTrip(@Query("trip_id") tripId: String): Response<TripApiResponse>
}
