import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class Day:
    """
    Generates fictional weather data forecast for a single day.
    """
    
    def __init__(self, base_temp: int = 22, temp_variance: int = 8):
        """
        Initialize the weather data generator.
        
        Args:
            base_temp (int): Base temperature around which to generate variations
            temp_variance (int): Maximum temperature variance from base temp
        """
        self.base_temp = base_temp
        self.temp_variance = temp_variance
        
    def _generate_hourly_temperature(self) -> List[int]:
        """
        Generate realistic hourly temperatures for 24 hours.
        
        Simulates natural temperature patterns with cooler temperatures
        in early morning and warmer in afternoon.
        
        Returns:
            List[int]: 24 hourly temperature values in Celsius
        """
        temps = []
        for hour in range(24):
            # Create natural temperature curve - cooler at night, warmer during day
            time_factor = -0.5 * ((hour - 14) / 12) ** 2 + 0.5  # Peak around 2 PM
            daily_variation = time_factor * self.temp_variance
            
            # Add some random variation
            random_variation = random.uniform(-2, 2)
            
            temp = int(self.base_temp + daily_variation + random_variation)
            temps.append(max(0, temp))  # Ensure no negative temperatures
            
        return temps
    
    def _generate_hourly_humidity(self) -> List[int]:
        """
        Generate realistic hourly humidity percentages.
        
        Returns:
            List[int]: 24 hourly humidity values as percentages (0-100)
        """
        base_humidity = random.randint(40, 80)
        humidity_values = []
        
        for hour in range(24):
            # Higher humidity in early morning, lower in afternoon
            time_factor = 0.3 * ((hour - 6) / 12) ** 2 - 0.3
            variation = random.uniform(-10, 10)
            
            humidity = int(base_humidity - time_factor * 20 + variation)
            humidity_values.append(max(20, min(100, humidity)))  # Clamp between 20-100
            
        return humidity_values
    
    def _generate_hourly_rainfall_chance(self) -> List[int]:
        """
        Generate hourly rainfall chance percentages.
        
        Returns:
            List[int]: 24 hourly rainfall chance values as percentages (0-100)
        """
        # Determine if it's a rainy day or not
        is_rainy_day = random.choice([True, False, False, False])  # 25% chance of rain
        
        rainfall_chances = []
        
        if is_rainy_day:
            # If rainy day, cluster rain around afternoon/evening
            peak_rain_hour = random.randint(12, 18)
            for hour in range(24):
                distance_from_peak = abs(hour - peak_rain_hour)
                base_chance = max(0, 80 - (distance_from_peak * 8))
                variation = random.uniform(-15, 15)
                chance = int(base_chance + variation)
                rainfall_chances.append(max(0, min(100, chance)))
        else:
            # Clear day with minimal rain chance
            for hour in range(24):
                chance = random.randint(0, 15)
                rainfall_chances.append(chance)
                
        return rainfall_chances
    
    def _generate_hourly_rainfall_amount(self, rainfall_chances: List[int]) -> List[float]:
        """
        Generate hourly rainfall amounts in mm based on rainfall chances.
        
        Args:
            rainfall_chances (List[int]): Rainfall chance percentages for each hour
            
        Returns:
            List[float]: 24 hourly rainfall amounts in mm
        """
        rainfall_amounts = []
        
        for chance in rainfall_chances:
            if chance < 20:
                # Very low chance - no rain
                amount = 0.0
            elif chance < 40:
                # Low chance - light drizzle
                amount = round(random.uniform(0.0, 1.0), 1)
            elif chance < 70:
                # Moderate chance - light to moderate rain
                amount = round(random.uniform(0.5, 5.0), 1)
            else:
                # High chance - moderate to heavy rain
                amount = round(random.uniform(2.0, 15.0), 1)
                
            rainfall_amounts.append(amount)
            
        return rainfall_amounts
    
    def weather(self) -> Dict[str, Any]:
        """
        Generate complete fictional weather data for today.
        
        Returns:
            Dict[str, Any]: Dictionary containing today's weather data with keys:
                - hourly_temp: List of 24 hourly temperatures (°C)
                - hourly_humidity: List of 24 hourly humidity percentages
                - hourly_rainfall_chance: List of 24 hourly rainfall chances (%)
                - hourly_rainfall_amount: List of 24 hourly rainfall amounts (mm)
        """        
        # Generate hourly data
        hourly_temp = self._generate_hourly_temperature()
        hourly_humidity = self._generate_hourly_humidity()
        hourly_rainfall_chance = self._generate_hourly_rainfall_chance()
        hourly_rainfall_amount = self._generate_hourly_rainfall_amount(hourly_rainfall_chance)
        
        # Calculate daily summary
        
        return {
            "hourly_temp": hourly_temp,
            "hourly_humidity": hourly_humidity,
            "hourly_rainfall_chance": hourly_rainfall_chance,
            "hourly_rainfall_amount": hourly_rainfall_amount,
        }
    
class WeatherEndpoint():
    """
    Generates fictional weather data forecast for a week.

    This class simulates a weather data endpoint by generating realistic
    but fictional weather data including hourly temperatures, humidity,
    rainfall chances and amounts for weekly forecasts.
    
    Attributes:
        today (int): Current day of the week (1=Monday, 7=Sunday)
    """
    # Get current day of week (1=Monday, 7=Sunday)
    def __init__(self):
        self.today = datetime.today().isoweekday()
    
    def current_week(self) -> Dict[datetime, Dict[str, Any]]:
        """
        Generate weather data for the current week.
        
        Returns a dictionary mapping each day of the current week
        (starting from Monday) to its weather data.
        
        Returns:
            Dict[datetime, Dict[str, Any]]: Dictionary with datetime keys
                representing each day of the current week, and values
                containing the weather data for that day
        """
        week_start = datetime.today() - timedelta(days=self.today)
        
        return {
            day.date() : Day().weather() for day in [week_start+timedelta(days=x) for x in range(7)]
        }
    
    def next_week(self) -> Dict[datetime, Dict[str, Any]]:
        """
        Generate weather data for the next week.
        
        Returns a dictionary mapping each day of the next week
        (starting from Monday) to its weather data.
        
        Returns:
            Dict[datetime, Dict[str, Any]]: Dictionary with datetime keys
                representing each day of the next week, and values
                containing the weather data for that day
        """
        week_start = datetime.today() + timedelta(days=7-self.today) 

        return {
            day.date() : Day().weather() for day in [week_start+timedelta(days=x) for x in range(7)]
        }
