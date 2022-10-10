import numpy as np

from constants import DEBUG


def save_dbg_img(img, name):
    if DEBUG:
        img.save(name)


def get_vector_angle(v1, v2):
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)

    if v1_norm == 0 or v2_norm == 0:
        return 0

    return np.arccos(np.clip(np.dot(v1, v2) / (v1_norm * v2_norm), -1.0, 1.0))