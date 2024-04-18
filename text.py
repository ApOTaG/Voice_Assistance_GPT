from pyowm import OWM

owm = OWM('1f66c8e5e26f3c18f7f14f3f49819a8c')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Kaunas,LT')
w = observation.weather
m = w.temperature('celsius')
print(m)
