import uos
import utime
from machine import ADC, Pin

# Constants
SAMPLE_RATE = 44100  # Adjust as needed
RECORD_SECONDS = 5
BUFFER_SIZE = 512  # Smaller buffer size

# ADC Configuration
adc = ADC(Pin(26))  # Use the appropriate pin for the microphone

# File to store audio data in flash memory
file_name = "audio_data.bin"

# Record audio data and save to file incrementally
print("Recording...")
start_time = utime.ticks_ms()
end_time = start_time + RECORD_SECONDS * 1000

with open(file_name, "wb") as file:
    while utime.ticks_ms() < end_time:
        remaining_samples = min(BUFFER_SIZE, (end_time - utime.ticks_ms()) * SAMPLE_RATE // 1000)
        audio_buffer = bytearray(remaining_samples * 2)  # 16-bit samples, 2 bytes per sample
        for i in range(remaining_samples):
            sample = adc.read_u16()
            audio_buffer[i * 2] = sample & 0xFF  # Low byte
            audio_buffer[i * 2 + 1] = (sample >> 8) & 0xFF  # High byte
        file.write(audio_buffer)

        # Add a small delay to avoid overwhelming the system
        utime.sleep_ms(10)

end_time_actual = utime.ticks_ms()
print("Recording complete. Time elapsed: {} seconds".format((end_time_actual - start_time) / 1000))

# List the files in flash memory to verify the saved file
print("\nFiles in flash memory:")
print(uos.listdir())
