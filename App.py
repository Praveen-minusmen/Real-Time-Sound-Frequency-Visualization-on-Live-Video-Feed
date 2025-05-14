import numpy as np
import sounddevice as sd
import librosa
import cv2

class SoundFrequencyVisualization:
    def __init__(self, sample_rate=44100):
        """
        Initialize the sound frequency visualization system.
        """
        self.sample_rate = sample_rate

    def record_audio(self, duration=1.0):
        """
        Record audio from the microphone.

        :param duration: Duration of the audio to record.
        :return: Recorded audio data.
        """
        audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32').flatten()
        sd.wait()
        return audio_data

    def extract_audio_frequency(self, audio_data):
        """
        Extract frequency components from audio.

        :param audio_data: The raw audio signal.
        :return: Frequencies and their corresponding amplitudes.
        """
        # Ensure the audio data does not contain non-finite values
        audio_data = np.nan_to_num(audio_data)

        # Normalize audio data to ensure it is within the appropriate range
        audio_data = np.clip(audio_data, -1.0, 1.0)

        # Compute Mel spectrogram
        S = librosa.feature.melspectrogram(y=audio_data, sr=self.sample_rate, n_mels=128, fmax=8000)

        # Ensure the spectrogram does not contain invalid values
        if np.any(np.isnan(S)) or np.any(np.isinf(S)):
            raise ValueError("Spectrogram contains non-finite values.")

        S_db = librosa.power_to_db(S, ref=np.max)
        return S_db

    def map_frequency_to_color(self, frequency_data):
        """
        Map frequency data to colors (red for high frequency, green for low frequency).

        :param frequency_data: The extracted frequency data.
        :return: Color-mapped image.
        """
        # Normalize the frequency data for visualization
        min_freq = np.min(frequency_data)
        max_freq = np.max(frequency_data)
        normalized_data = (frequency_data - min_freq) / (max_freq - min_freq)

        # Handle edge case where max_freq == min_freq
        if max_freq == min_freq:
            normalized_data = np.zeros_like(frequency_data)

        # Initialize the output image with black
        color_image = np.zeros((frequency_data.shape[0], frequency_data.shape[1], 3), dtype=np.uint8)

        # Assign color values based on frequency intensity
        for i in range(frequency_data.shape[0]):
            for j in range(frequency_data.shape[1]):
                intensity = normalized_data[i, j]
                if intensity > 0.5:
                    # High-frequency region (Red)
                    color_image[i, j] = [intensity * 255, 0, 0]  # Red
                else:
                    # Low-frequency region (Green)
                    color_image[i, j] = [0, intensity * 255, 0]  # Green

        return color_image

    def visualize_audio_on_video(self, frame, color_image):
        """
        Visualize the frequency data on the video feed by blending it with the live feed.

        :param frame: The current video frame.
        :param color_image: The frequency-to-color mapped image.
        :return: The blended frame.
        """
        # Resize the color image to match the video frame size
        color_image_resized = cv2.resize(color_image, (frame.shape[1], frame.shape[0]))
        
        # Blend the frequency color image with the original frame
        blended_frame = cv2.addWeighted(frame, 0.7, color_image_resized, 0.3, 0)
        return blended_frame


def main():
    # Initialize the sound frequency visualization system
    visualizer = SoundFrequencyVisualization()

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Record audio data
        audio_data = visualizer.record_audio(duration=1.0)

        try:
            # Extract frequency data from the audio
            frequency_data = visualizer.extract_audio_frequency(audio_data)
        except ValueError as e:
            print(f"Error with audio data: {e}")
            continue  # Skip this iteration and continue recording audio

        # Map the frequency data to colors (Red for high frequency, Green for low frequency)
        color_image = visualizer.map_frequency_to_color(frequency_data)

        # Capture the frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Visualize the frequency data on the live feed
        blended_frame = visualizer.visualize_audio_on_video(frame, color_image)

        # Display the live feed with frequency color grading
        cv2.imshow('Live Camera Feed with Sound Frequency Grading', blended_frame)

        # Check for exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
