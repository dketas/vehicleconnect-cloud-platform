"""
Vehicle Event Simulator
Generates realistic API traffic to test the system under load.
"""

import random
import time
import requests
from datetime import datetime
from typing import List

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Change to your AWS URL later

# Realistic vehicle API endpoints
ENDPOINTS = [
    "/api/vehicle/status",
    "/api/vehicle/location",
    "/api/vehicle/diagnostics",
    "/api/charging/status",
    "/api/remote/lock",
    "/api/remote/climate",
    "/api/navigation/route",
    "/api/user/profile",
]

METHODS = ["GET", "POST", "PUT", "DELETE"]

# 100 vehicle IDs
CLIENT_IDS = [f"vehicle_{i:05d}" for i in range(1, 101)]


def generate_realistic_latency(endpoint: str) -> float:
    """
    Generate realistic response times based on endpoint.
    Location lookups take longer than status checks.
    """
    latencies = {
        "status": (20, 80),        # Fast
        "location": (50, 200),     # GPS lookup
        "diagnostics": (100, 400), # Heavy computation
        "charging": (40, 120),     # Moderate
        "lock": (30, 100),         # Fast
        "climate": (60, 250),      # HVAC control
        "route": (200, 800),       # Route calculation
        "profile": (25, 90),       # Fast
    }
    
    for key, (min_lat, max_lat) in latencies.items():
        if key in endpoint.lower():
            return round(random.uniform(min_lat, max_lat), 2)
    
    # Default
    return round(random.uniform(30, 150), 2)


def generate_status_code() -> tuple[int, bool, str | None]:
    """
    98% success rate, realistic error distribution.
    """
    rand = random.random()
    
    if rand < 0.98:  # 98% success
        return 200, True, None
    elif rand < 0.99:  # 1% client errors
        codes = [400, 401, 403, 404, 429]
        return random.choice(codes), False, "Client error"
    else:  # 1% server errors
        codes = [500, 502, 503, 504]
        return random.choice(codes), False, "Server error"


def send_single_event():
    """
    Send one realistic vehicle API event.
    """
    endpoint = random.choice(ENDPOINTS)
    method = random.choice(METHODS)
    client_id = random.choice(CLIENT_IDS)
    
    response_time = generate_realistic_latency(endpoint)
    status_code, success, error_msg = generate_status_code()
    
    event_data = {
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "response_time_ms": response_time,
        "client_id": client_id,
        "error_message": error_msg,
        "success": success,
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/events",
            json=event_data,
            timeout=10,
            headers={"User-Agent": f"VehicleConnect-Simulator/{random.randint(1,10)}"}
        )
        
        if response.status_code == 201:
            print(f"✅ {method} {endpoint} ({client_id}) → {status_code} ({response_time}ms)")
        else:
            print(f"❌ {method} {endpoint} → HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"💥 Network error: {e}")


def simulate_traffic(
    duration_minutes: int = 5,
    events_per_second: float = 2.0,
    print_progress: bool = True,
):
    """
    Simulate realistic vehicle traffic for specified duration.
    """
    duration_seconds = duration_minutes * 60
    sleep_interval = 1.0 / events_per_second
    
    print(f"🚗 Starting VehicleConnect traffic simulation...")
    print(f"📊 Duration: {duration_minutes} minutes")
    print(f"⚡ Rate: {events_per_second} events/sec")
    print(f"🌐 Target: {API_BASE_URL}")
    print(f"{'─' * 60}")
    
    start_time = time.time()
    event_count = 0
    
    try:
        while time.time() - start_time < duration_seconds:
            send_single_event()
            event_count += 1
            
            # Progress every 20 events
            if print_progress and event_count % 20 == 0:
                elapsed = time.time() - start_time
                actual_rate = event_count / elapsed
                print(f"📈 {event_count} events | {actual_rate:.1f} eps | {elapsed:.0f}s elapsed")
            
            time.sleep(sleep_interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
    
    total_time = time.time() - start_time
    final_rate = event_count / total_time if total_time > 0 else 0
    
    print(f"{'─' * 60}")
    print(f"✅ Simulation complete!")
    print(f"📊 Total events: {event_count:,}")
    print(f"⚡ Average rate: {final_rate:.1f} eps")
    print(f"⏱️  Duration: {total_time:.1f} seconds")
    print(f"💾 Check: http://127.0.0.1:8000/api/events")
    print(f"📈 Metrics: http://127.0.0.1:8000/metrics")


if __name__ == "__main__":
    simulate_traffic(duration_minutes=5, events_per_second=2.0)
