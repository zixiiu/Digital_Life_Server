# KaldiFeat

KaldiFeat is a light-weight Python library for computing Kaldi-style acoustic features based on NumPy. It might be helpful if you want to:

- Test a pre-trained model on new data without writing shell commands and creating a bunch of files.
- Run a pre-trained model in a new environment without installing Kaldi.

## Example

The following codes calculate MFCCs with the same settings in `kaldi/egs/voxceleb/v2`

```
import librosa

from kaldifeat import compute_mfcc_feats, compute_vad, apply_cmvn_sliding

# Assume we have a wav file called example.wav whose sample rate is 16000 Hz
data, _ = librosa.load('example.wav', 16000)

# We adopt 16 bits data, thus we need to transform dtype from float to int16 for librosa
data = (data * 32768).astype(np.int16)

raw_mfcc = compute_mfcc_feats(data, sample_frequency=16000, frame_length=25, frame_shift=10, low_freq=20, high_freq=-400, num_mel_bins=30, num_ceps=30, snip_edges=False)
log_energy = raw_mfcc[:, 0]
vad = compute_vad(log_energy, energy_threshold=5.5, energy_mean_scale=0.5, frames_context=2, proportion_threshold=0.12)
mfcc = apply_cmvn_sliding(raw_mfcc, window=300, center=True)[vad]
```

## Supported Functions

### compute_fbank_feats

Compute (log) Mel filter bank energies (FBanks) in the same way as `kaldi/src/featbin/compute_fbank_feats`

| Parameters | Description |
| :--------- | :---------- |
|blackman_coeff| Constant coefficient for generalized Blackman window. (float, default = 0.42)|
|dither| Dithering constant (0.0 means no dither). If you turn this off, you should set the --energy-floor option, e.g. to 1.0 or 0.1 (float, default = 1)|
|energy_floor| Floor on energy (absolute, not relative) in FBANK computation. Only makes a difference if --use-energy=true; only necessary if --dither=0.0.  Suggested values: 0.1 or 1.0 (float, default = 0)|
|frame_length| Frame length in milliseconds (float, default = 25)|
|frame_shift| Frame shift in milliseconds (float, default = 10)|
|high_freq| High cutoff frequency for mel bins (if <= 0, offset from Nyquist) (float, default = 0)|
|low_freq| Low cutoff frequency for mel bins (float, default = 20)|
|num_mel_bins| Number of triangular mel-frequency bins (int, default = 23)|
|preemphasis_coefficient| Coefficient for use in signal preemphasis (float, default = 0.97)|
|raw_energy| If true, compute energy before preemphasis and windowing (bool, default = true)|
|remove_dc_offset| Subtract mean from waveform on each frame (bool, default = true)|
|round_to_power_of_two| If true, round window size to power of two by zero-padding input to FFT. (bool, default = true)|
|sample_frequency| Waveform data sample frequency (must match the waveform file, if specified there) (float, default = 16000)|
|snip_edges| If true, end effects will be handled by outputting only frames that completely fit in the file, and the number of frames depends on the frame-length.  If false, the number of frames depends only on the frame-shift, and we reflect the data at the ends. (bool, default = true)|
|use_energy| Add an extra energy output. (bool, default = false)|
|use_log_fbank| If true, produce log-filterbank, else produce linear. (bool, default = true)|
|use_power| If true, use power, else use magnitude. (bool, default = true)|
|window_type| Type of window ("hamming"\|"hanning"\|"povey"\|"rectangular"\|"sine"\|"blackmann") (string, default = "povey")|
|dtype| Type of array (np.float32\|np.float64) (dtype or string, default=np.float32)|

### compute_mfcc_feats

Compute Mel-frequency cepstral coefficients (MFCCs) in the same way as `kaldi/src/featbin/compute_mfcc_feats`

| Parameters | Description |
| :--------- | :---------- |
|blackman_coeff| Constant coefficient for generalized Blackman window. (float, default = 0.42)|
|cepstral_lifter| Constant that controls scaling of MFCCs (float, default = 22)|
|dither| Dithering constant (0.0 means no dither). If you turn this off, you should set the --energy-floor option, e.g. to 1.0 or 0.1 (float, default = 1)|
|energy_floor| Floor on energy (absolute, not relative) in MFCC computation. Only makes a difference if --use-energy=true; only necessary if --dither=0.0.  Suggested values: 0.1 or 1.0 (float, default = 0)|
|frame_length| Frame length in milliseconds (float, default = 25)|
|frame_shift| Frame shift in milliseconds (float, default = 10)|
|high_freq| High cutoff frequency for mel bins (if <= 0, offset from Nyquist) (float, default = 0)|
|low_freq| Low cutoff frequency for mel bins (float, default = 20)|
|num_ceps| Number of cepstra in MFCC computation (including C0) (int, default = 13)|
|num_mel_bins| Number of triangular mel-frequency bins (int, default = 23)|
|preemphasis_coefficient| Coefficient for use in signal preemphasis (float, default = 0.97)|
|raw_energy| If true, compute energy before preemphasis and windowing (bool, default = true)|
|remove_dc_offset| Subtract mean from waveform on each frame (bool, default = true)|
|round_to_power_of_two| If true, round window size to power of two by zero-padding input to FFT. (bool, default = true)|
|sample_frequency| Waveform data sample frequency (must match the waveform file, if specified there) (float, default = 16000)|
|snip_edges| If true, end effects will be handled by outputting only frames that completely fit in the file, and the number of frames depends on the frame-length.  If false, the number of frames depends only on the frame-shift, and we reflect the data at the ends. (bool, default = true)|
|use_energy| Use energy (not C0) in MFCC computation (bool, default = true)|
|window_type| Type of window ("hamming"\|"hanning"\|"povey"\|"rectangular"\|"sine"\|"blackmann") (string, default = "povey")|
|dtype| Type of array (np.float32\|np.float64) (dtype or string, default=np.float32)|

### apply_cmvn_sliding

Apply sliding-window cepstral mean (and optionally variance) normalization in the same way as `kaldi/src/featbin/apply_cmvn_sliding`

| Parameters | Description |
| :--------- | :---------- |
|center| If true, use a window centered on the current frame (to the extent possible, modulo end effects). If false, window is to the left. (bool, default = false)|
|window| Window in frames for running average CMN computation (int, default = 600)|
|min_window| Minimum CMN window used at start of decoding (adds latency only at start). Only applicable if center == false, ignored if center==true (int, default = 100)|
|norm_vars| If true, normalize variance to one. (bool, default = false)|

### compute_vad

Apply energy-based voice activity detection in the same way as `kaldi/src/ivectorbin/compute_vad`

| Parameters | Description |
| :--------- | :---------- |
|energy_mean_scale| If this is set to s, to get the actual threshold we let m be the mean log-energy of the file, and use s\*m + vad-energy-threshold (float, default = 0.5)|
|energy_threshold| Constant term in energy threshold for VAD (also see energy_mean_scale) (float, default = 5)|
|frames_context| Number of frames of context on each side of central frame, in window for which energy is monitored (int, default = 0)|
|proportion_threshold| Parameter controlling the proportion of frames within the window that need to have more energy than the threshold (float, default = 0.6)|

### Related Projects

- [python_speech_features](https://github.com/jameslyons/python_speech_features)
- [python_kaldi_features](https://github.com/ZitengWang/python_kaldi_features)
