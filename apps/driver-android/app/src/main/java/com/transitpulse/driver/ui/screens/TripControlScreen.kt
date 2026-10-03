package com.transitpulse.driver.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun TripControlScreen() {
    var isTripActive by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Route: Hubballi CBT to Dharwad BRTS", style = MaterialTheme.typography.titleMedium)
        Text("Bus: KA-25-F-1001", style = MaterialTheme.typography.bodyMedium)
        Spacer(modifier = Modifier.height(32.dp))

        if (!isTripActive) {
            Button(
                onClick = { isTripActive = true },
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("START TRIP")
            }
        } else {
            Button(
                onClick = { isTripActive = false },
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("STOP TRIP")
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("GPS Beacon Active • Emitting fixes every 5s", color = MaterialTheme.colorScheme.secondary)
        }
    }
}
