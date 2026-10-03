package com.transitpulse.driver.viewmodel

import androidx.lifecycle.ViewModel

class TripViewModel : ViewModel() {
    var isTripActive: Boolean = false
    var activeTripId: String? = null
}
