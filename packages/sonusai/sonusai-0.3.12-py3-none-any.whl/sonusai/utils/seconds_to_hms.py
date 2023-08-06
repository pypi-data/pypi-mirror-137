def seconds_to_hms(seconds: float) -> str:
    h = int(seconds / 3600)
    s = seconds - h * 3600
    m = int(s / 60)
    s = int(seconds - h * 3600 - m * 60)
    return '{:d}:{:02d}:{:02d} (H:MM:SS)'.format(h, m, s)
