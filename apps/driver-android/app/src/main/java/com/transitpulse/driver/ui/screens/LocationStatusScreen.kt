package com.transitpulse.driver.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun LocationStatusScreen() {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Location & Sync Status", style = MaterialTheme.typography.titleLarge)
        Spacer(modifier = Modifier.height(16.dp))
        Text("GPS Permission: GRANTED (High Accuracy)")
        Text("Network Status: Connected (4G)")
        Text("Offline Queued Points: 0")
        Text("Last Signal: 2 seconds ago")
    }
}
