package com.transitpulse.driver.viewmodel

import androidx.lifecycle.ViewModel

class AuthViewModel : ViewModel() {
    fun login(email: String, pass: String): Boolean {
        return true
    }
}
