# Real-Time-Sound-Frequency-Visualization-on-Live-Video-Feed

This project captures audio from your microphone, analyzes its frequency components, and visualizes them as color overlays on a live camera feed. High-frequency sounds are mapped to red, while low-frequency sounds are mapped to green, providing an intuitive way to "see" sound in real time.

## Features

- **Real-time audio recording** from your microphone.
- **Frequency analysis** using Mel spectrograms.
- **Color mapping**: Red for high frequencies, green for low frequencies.
- **Live video blending**: Overlays the frequency visualization on your webcam feed.
- **Easy exit**: Press `q` to quit the application.

## Requirements

- Python 3.7+
- numpy
- sounddevice
- librosa
- opencv-python

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required packages:
    ```bash
    pip install numpy sounddevice librosa opencv-python
    ```

## Usage

Run the main script:
```bash
python App.py
```

- Make sure your microphone and webcam are connected and accessible.
- The application will open a window showing your live camera feed with sound frequency visualization.
- Press `q` to exit.

## How it Works

1. **Audio Recording**: Captures 1-second audio samples from the microphone.
2. **Frequency Extraction**: Computes the Mel spectrogram of the audio.
3. **Color Mapping**: Maps frequency intensities to colors (red/green).
4. **Video Blending**: Overlays the color map onto the live camera frame.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [librosa](https://librosa.org/) for audio analysis.
- [OpenCV](https://opencv.org/) for video processing.
- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio recording.
