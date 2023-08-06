import numpy as np
from scipy.io import wavfile
from scipy import interpolate
import librosa
import pyworld
import pysptk


def pad1d(x, max_len, constant_values=0):
    """Pad a 1d-tensor.

    Args:
        x (torch.Tensor): tensor to pad
        max_len (int): maximum length of the tensor
        constant_values (int, optional): value to pad with. Default: 0

    Returns:
        torch.Tensor: padded tensor
    """
    x = np.pad(
        x,
        (0, max_len - len(x)),
        mode="constant",
        constant_values=constant_values,
    )
    return x

    
#### wav #### 
def load_wav(path):
    sr, x = wavfile.read(path)
    signed_int16_max = 2**15
    if x.dtype == np.int16:
        x = x.astype(np.float32) / signed_int16_max
    x = np.clip(x, -1.0, 1.0)
    return sr, x

def resample(x, sr, target_sr):
    return librosa.resample(x, sr, target_sr)


def low_cut_filter(x, fs, cutoff=70):
    """APPLY LOW CUT FILTER.

    https://github.com/kan-bayashi/PytorchWaveNetVocoder

    Args:
        x (ndarray): Waveform sequence.
        fs (int): Sampling frequency.
        cutoff (float): Cutoff frequency of low cut filter.
    Return:
        ndarray: Low cut filtered waveform sequence.
    """
    nyquist = fs // 2
    norm_cutoff = cutoff / nyquist
    from scipy.signal import firwin, lfilter

    # low cut filter
    fil = firwin(255, norm_cutoff, pass_zero=False)
    lcf_x = lfilter(fil, 1, x)

    return lcf_x


#### mulaw-quantize #### 
def mulaw(x, mu=255):
    """Mu-Law companding.

    Args:
        x (ndarray): Input signal.
        mu (int): Mu.

    Returns:
        ndarray: Compressed signal.
    """
    return np.sign(x) * np.log1p(mu * np.abs(x)) / np.log1p(mu)


def quantize(y, mu=255, offset=1):
    """Quantize the signal

    Args:
        y (ndarray): Input signal.
        mu (int): Mu.
        offset (int): Offset.

    Returns:
        ndarray: Quantized signal.
    """
    # [-1, 1] -> [0, 2] -> [0, 1] -> [0, mu]
    return ((y + offset) / 2 * mu).astype(np.int64)


def mulaw_quantize(x, mu=255):
    """Mu-law-quantize signal.

    Args:
        x (ndarray): Input signal.
        mu (int): Mu.

    Returns:
        ndarray: Quantized signal.
    """
    return quantize(mulaw(x, mu), mu)


#### logmelspec #### 
"""Same log-melspectrogram computation as espnet
https://github.com/espnet/espnet
from espnet.transform.spectrogram import logmelspectrogram
"""
def stft(
    x, n_fft, n_shift, win_length=None, window="hann", center=True, pad_mode="reflect"
):
    # x: [Time, Channel]
    if x.ndim == 1:
        single_channel = True
        # x: [Time] -> [Time, Channel]
        x = x[:, None]
    else:
        single_channel = False
    x = x.astype(np.float32)

    # FIXME(kamo): librosa.stft can't use multi-channel?
    # x: [Time, Channel, Freq]
    x = np.stack(
        [
            librosa.stft(
                x[:, ch],
                n_fft=n_fft,
                hop_length=n_shift,
                win_length=win_length,
                window=window,
                center=center,
                pad_mode=pad_mode,
            ).T
            for ch in range(x.shape[1])
        ],
        axis=1,
    )

    if single_channel:
        # x: [Time, Channel, Freq] -> [Time, Freq]
        x = x[:, 0]

    return x


def stft2logmelspectrogram(x_stft, fs, n_mels, n_fft, fmin=None, fmax=None, eps=1e-10):
    # x_stft: (Time, Channel, Freq) or (Time, Freq)
    fmin = 0 if fmin is None else fmin
    fmax = fs / 2 if fmax is None else fmax

    # spc: (Time, Channel, Freq) or (Time, Freq)
    spc = np.abs(x_stft)
    # mel_basis: (Mel_freq, Freq)
    mel_basis = librosa.filters.mel(fs, n_fft, n_mels, fmin, fmax)
    # lmspc: (Time, Channel, Mel_freq) or (Time, Mel_freq)
    lmspc = np.log10(np.maximum(eps, np.dot(spc, mel_basis.T)))

    return lmspc


def spectrogram(x, n_fft, n_shift, win_length=None, window="hann"):
    # x: (Time, Channel) -> spc: (Time, Channel, Freq)
    spc = np.abs(stft(x, n_fft, n_shift, win_length, window=window))
    return spc


def logmelspectrogram(
    x,
    fs,
    n_mels,
    n_fft,
    n_shift,
    win_length=None,
    window="hann",
    fmin=None,
    fmax=None,
    eps=1e-10,
    pad_mode="reflect",
):

    # stft: (Time, Channel, Freq) or (Time, Freq)
    x_stft = stft(
        x,
        n_fft=n_fft,
        n_shift=n_shift,
        win_length=win_length,
        window=window,
        pad_mode=pad_mode,
    )

    return stft2logmelspectrogram(
        x_stft, fs=fs, n_mels=n_mels, n_fft=n_fft, fmin=fmin, fmax=fmax, eps=eps
    )


### delta features ###

def _delta(x, window):
    return np.correlate(x, window, mode="same")


def _apply_delta_window(x, window):
    """Returns delta features given a static features and a window.

    Args:
        x (numpy.ndarray): Input static features, of shape (``T x D``).
        window (numpy.ndarray): Window coefficients.

    Returns:
        (ndarray): Delta features, shape (``T x D``).
    """
    T, D = x.shape
    y = np.zeros_like(x)
    for d in range(D):
        y[:, d] = _delta(x[:, d], window)
    return y


def delta_features(x, windows):
    """Compute delta features and combine them.

    This function computes delta features given delta windows, and then
    returns combined features (e.g., static + delta + delta-delta).
    Note that if you want to keep static features, you need to give
    static window as well as delta windows.

    Args:
        x (numpy.ndarray): Input static features, of shape (``T x D``).
        y (list): List of windows. See :func:`nnmnkwii.paramgen.mlpg` for what
            the delta window means.

    Returns:
        numpy.ndarray: static + delta features (``T x (D * len(windows)``).

    Examples:
        >>> from nnmnkwii.preprocessing import delta_features
        >>> windows = [
        ...         (0, 0, np.array([1.0])),            # static
        ...         (1, 1, np.array([-0.5, 0.0, 0.5])), # delta
        ...         (1, 1, np.array([1.0, -2.0, 1.0])), # delta-delta
        ...     ]
        >>> T, static_dim = 10, 24
        >>> x = np.random.rand(T, static_dim)
        >>> y = delta_features(x, windows)
        >>> assert y.shape == (T, static_dim * len(windows))
    """
    T, D = x.shape
    assert len(windows) > 0
    combined_features = np.empty((T, D * len(windows)), dtype=x.dtype)
    # NOTE: bandmat case
    if isinstance(windows[0], tuple):
        for idx, (_, _, window) in enumerate(windows):
            combined_features[:, D * idx : D * idx + D] = _apply_delta_window(x, window)
    else:
        for idx, window in enumerate(windows):
            combined_features[:, D * idx : D * idx + D] = _apply_delta_window(x, window)
    return combined_features


def calc_delta_features(x):
    # 動的特徴量の計算
    windows = [
        [1.0],  # 静的特徴量に対する窓
        [-0.5, 0.0, 0.5],  # 1次動的特徴量に対する窓
        [1.0, -2.0, 1.0],  # 2次動的特徴量に対する窓
    ]
    return delta_features(x, windows)


### world spss params ###
def interp1d(f0, kind="slinear"):
    """Coutinuous F0 interpolation from discontinuous F0 trajectory

    This function generates continuous f0 from discontinuous f0 trajectory
    based on :func:`scipy.interpolate.interp1d`. This is meant to be used for
    continuous f0 modeling in statistical speech synthesis
    (e.g., see [1]_, [2]_).

    If ``kind`` = ``'slinear'``, then this does same thing as Merlin does.

    Args:
        f0 (ndarray): F0 or log-f0 trajectory
        kind (str): Kind of interpolation that :func:`scipy.interpolate.interp1d`
            supports. Default is ``'slinear'``, which means linear interpolation.

    Returns:
        1d array (``T``, ) or 2d (``T`` x 1) array: Interpolated continuous f0
        trajectory.

    Examples:
        >>> from nnmnkwii.preprocessing import interp1d
        >>> import numpy as np
        >>> from nnmnkwii.util import example_audio_file
        >>> from scipy.io import wavfile
        >>> import pyworld
        >>> fs, x = wavfile.read(example_audio_file())
        >>> f0, timeaxis = pyworld.dio(x.astype(np.float64), fs, frame_period=5)
        >>> continuous_f0 = interp1d(f0, kind="slinear")
        >>> assert f0.shape == continuous_f0.shape

    .. [1] Yu, Kai, and Steve Young. "Continuous F0 modeling for HMM based
        statistical parametric speech synthesis." IEEE Transactions on Audio,
        Speech, and Language Processing 19.5 (2011): 1071-1079.

    .. [2] Takamichi, Shinnosuke, et al. "The NAIST text-to-speech system for
        the Blizzard Challenge 2015." Proc. Blizzard Challenge workshop. 2015.
    """
    ndim = f0.ndim
    if len(f0) != f0.size:
        raise RuntimeError("1d array is only supported")
    continuous_f0 = f0.flatten()
    nonzero_indices = np.where(continuous_f0 > 0)[0]

    # Nothing to do
    if len(nonzero_indices) <= 0:
        return f0

    # Need this to insert continuous values for the first/end silence segments
    continuous_f0[0] = continuous_f0[nonzero_indices[0]]
    continuous_f0[-1] = continuous_f0[nonzero_indices[-1]]

    # Build interpolation function
    nonzero_indices = np.where(continuous_f0 > 0)[0]
    interp_func = interpolate.interp1d(
        nonzero_indices, continuous_f0[continuous_f0 > 0], kind=kind
    )

    # Fill silence segments with interpolated values
    zero_indices = np.where(continuous_f0 <= 0)[0]
    continuous_f0[zero_indices] = interp_func(zero_indices)

    if ndim == 2:
        return continuous_f0[:, None]
    return continuous_f0


def f0_to_lf0(f0):
    """Convert F0 to log-F0

    Args:
        f0 (ndarray): F0 in Hz.

    Returns:
        ndarray: log-F0.
    """
    lf0 = f0.copy()
    nonzero_indices = np.nonzero(f0)
    lf0[nonzero_indices] = np.log(f0[nonzero_indices])
    return lf0


def lf0_to_f0(lf0, vuv):
    """Convert log-F0 (and V/UV) to F0

    Args:
        lf0 (ndarray): F0 in Hz.
        vuv (ndarray): V/UV.

    Returns:
        ndarray: F0 in Hz.
    """
    f0 = np.exp(lf0)
    f0[vuv < 0.5] = 0
    return f0


def world_spss_params(
    x, sr, 
    frame_shifts=None, 
    mgc_order=None, 
    lf0interp=False, 
    use_delta_features=False):
    """WORLD-based acoustic feature extraction

    Args:
        x (ndarray): Waveform.
        sr (int): Sampling rate.
        mgc_order (int, optional): MGC order. Defaults to None.
        lf0interp (bool) : use or unuse lf0 interpolation
        use_delta_features (bool) : use or unuse delta features

    Returns:
        ndarray: WORLD features.
    """
    if frame_shifts is None:
        f0, timeaxis = pyworld.dio(x, sr)
    else:
        f0, timeaxis = pyworld.dio(x, sr, frame_period=frame_shifts*1000)

    # (Optinal) Stonemask によってF0の推定結果をrefineする
    f0 = pyworld.stonemask(x, f0, timeaxis, sr)

    sp = pyworld.cheaptrick(x, f0, timeaxis, sr)
    ap = pyworld.d4c(x, f0, timeaxis, sr)

    alpha = pysptk.util.mcepalpha(sr)
    # メルケプストラムの次元数（※過去の論文にならい、16kHzの際に
    # 次元数が40（mgc_order + 1）になるように設定する
    # ただし、上限を 60 (59 + 1) とする
    # [Zen 2013] Statistical parametric speech synthesis using deep neural networks
    if mgc_order is None:
        mgc_order = min(int(sr / 16000.0 * 40) - 1, 59)
    mgc = pysptk.sp2mc(sp, mgc_order, alpha)

    # 対数F0
    lf0 = f0_to_lf0(f0)
    if lf0interp is True:
        lf0 = interp1d(lf0)

    # 有声/無声フラグ
    vuv = (f0 > 0).astype(np.float32)

    # 帯域非周期性指標
    bap = pyworld.code_aperiodicity(ap, sr)

    # F0とvuvを二次元の行列の形にしておく
    lf0 = lf0[:, np.newaxis] if len(lf0.shape) == 1 else lf0
    vuv = vuv[:, np.newaxis] if len(vuv.shape) == 1 else vuv

    if use_delta_features is True:
        mgc = calc_delta_features(mgc)
        lf0 = calc_delta_features(lf0)
        bap = calc_delta_features(bap)

    return mgc, lf0, vuv, bap


def world_f0_vuv(
    x, sr, 
    logf0=False,
    frame_shifts=None,
    f0interp=False, 
    use_delta_features=False):
    """WORLD-based acoustic feature extraction

    Args:
        x (ndarray): Waveform.
        sr (int): Sampling rate.
        logf0(bool) : use f0 or logf0 
        frame_shifts (float) : analysis frame_shift of WORLD (sec)
        f0interp (bool) : use or unuse f0 interpolation
        use_delta_features (bool) : use or unuse delta features

    Returns:
        ndarray: WORLD features.
    """
    if frame_shifts is None:
        f0, timeaxis = pyworld.dio(x, sr)
    else:
        f0, timeaxis = pyworld.dio(x, sr, frame_period=frame_shifts*1000)

    # (Optinal) Stonemask によってF0の推定結果をrefineする
    f0 = pyworld.stonemask(x, f0, timeaxis, sr)
    # 対数F0
    if logf0 is True:
        f0 = f0_to_lf0(f0)
    if f0interp is True:
        f0 = interp1d(f0)

    # 有声/無声フラグ
    vuv = (f0 > 0).astype(np.float32)

    # F0とvuvを二次元の行列の形にしておく
    f0 = f0[:, np.newaxis] if len(f0.shape) == 1 else f0
    vuv = vuv[:, np.newaxis] if len(vuv.shape) == 1 else vuv

    if use_delta_features is True:
        # 動的特徴量の計算
        f0 = calc_delta_features(f0)
        
    return f0, vuv
