def spec_kw_fft_ph(omega, V, E, ee):
    # Ensure V is shaped correctly
    total_expected = 2 * (int(np.sqrt(V.size / (2 * V.shape[1]))) ** 2)
    if V.shape[0] == total_expected * V.shape[1]:  # Flattened
        raise ValueError("V appears to be flattened incorrectly.")
    
    N_guess = int(np.sqrt(V.shape[0] / 2)) if V.shape[0] % 2 == 0 else None
    if N_guess is None:
        raise ValueError("V has incompatible shape for splitting into u/v.")

    # Transpose if 2*N² is along axis 1 instead of axis 0
    if V.shape[1] == 2 * N_guess**2:
        V = V.T

    # Trim if too big
    needed_rows = 2 * N_guess**2
    if V.shape[0] > needed_rows:
        V = V[:needed_rows, :]
    elif V.shape[0] < needed_rows:
        raise ValueError(f"V too small: {V.shape[0]} rows, expected {needed_rows}.")

    u = V[:N_guess**2, :]
    v = V[N_guess**2:, :]
    u = u.reshape((N_guess, N_guess, V.shape[1]))
    v = v.reshape((N_guess, N_guess, V.shape[1]))

    d = 0
    if d > 0:
        N_guess -= 2 * d
        u = u[d:-d, d:-d, :]
        v = v[d:-d, d:-d, :]

    L1 = ee / ((omega - E) ** 2 + ee ** 2) / np.pi
    L2 = ee / ((omega + E) ** 2 + ee ** 2) / np.pi

    u_fft = np.abs(np.fft.fft2(u, axes=(0, 1))) ** 2
    v_fft = np.abs(np.fft.fft2(v, axes=(0, 1))) ** 2

    u_fft = u_fft.reshape((N_guess**2, V.shape[1]))
    v_fft = v_fft.reshape((N_guess**2, V.shape[1]))

    h = np.fft.fftshift((u_fft @ L1).reshape((N_guess, N_guess))) / (N_guess**2)
    p = np.fft.fftshift((v_fft @ L2).reshape((N_guess, N_guess))) / (N_guess**2)

    return p, h


def spec_kw_fft_w(V, E, ee):
    N_guess = int(np.sqrt(V.shape[0] / 2))

    # Transpose if needed
    if V.shape[1] == 2 * N_guess**2:
        V = V.T

    needed_rows = 2 * N_guess**2
    if V.shape[0] > needed_rows:
        V = V[:needed_rows, :]
    elif V.shape[0] < needed_rows:
        raise ValueError(f"V too small: {V.shape[0]} rows, expected {needed_rows}.")

    w = np.linspace(-1.5, 1.5, 501)

    u = V[:N_guess**2, :]
    v = V[N_guess**2:, :]
    u = u.reshape((N_guess, N_guess, V.shape[1]))
    v = v.reshape((N_guess, N_guess, V.shape[1]))

    d = 0
    if d > 0:
        N_guess -= 2 * d
        u = u[d:-d, d:-d, :]
        v = v[d:-d, d:-d, :]

    u_fft = np.abs(np.fft.fft2(u, axes=(0, 1))) ** 2
    v_fft = np.abs(np.fft.fft2(v, axes=(0, 1))) ** 2

    u_fft = u_fft.reshape((N_guess**2, V.shape[1]))
    v_fft = v_fft.reshape((N_guess**2, V.shape[1]))

    xv, yv = np.meshgrid(w, E)
    wp = xv + yv
    wm = xv - yv

    L2 = ee / (wp**2 + ee**2) / np.pi
    L1 = ee / (wm**2 + ee**2) / np.pi

    h = np.fft.fftshift((u_fft @ L1).reshape((N_guess, N_guess, w.shape[0]))) / (N_guess**2)
    p = np.fft.fftshift((v_fft @ L2).reshape((N_guess, N_guess, w.shape[0]))) / (N_guess**2)

    return p, h
