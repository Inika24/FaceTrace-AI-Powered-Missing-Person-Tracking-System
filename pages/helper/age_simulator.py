import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from pages.helper.utils import extract_face_mesh_landmarks

def _apply_hair_greying(img_rgb: np.ndarray, face_box: tuple, years: int) -> np.ndarray:
    """Apply soft, realistic silver/grey highlights to hair region (top of head)."""
    h, w, _ = img_rgb.shape
    x_min, y_min, x_max, y_max = face_box
    
    hair_top = max(0, int(y_min - (y_max - y_min) * 0.4))
    hair_bottom = max(0, int(y_min + (y_max - y_min) * 0.12))
    hair_left = max(0, int(x_min - (x_max - x_min) * 0.15))
    hair_right = min(w, int(x_max + (x_max - x_min) * 0.15))
    
    if hair_bottom <= hair_top or hair_right <= hair_left:
        return img_rgb
        
    hair_roi = img_rgb[hair_top:hair_bottom, hair_left:hair_right].copy()
    gray_roi = cv2.cvtColor(hair_roi, cv2.COLOR_RGB2GRAY)
    
    # Target dark hair strands smoothly
    hair_mask = (gray_roi < 130).astype(np.float32)
    hair_mask = cv2.GaussianBlur(hair_mask, (25, 25), 0)
    
    hsv_roi = cv2.cvtColor(hair_roi, cv2.COLOR_RGB2HSV).astype(np.float32)
    grey_factor = min(0.4, (years / 20.0) * 0.35)
    
    # Soft desaturation and slight brightness boost for natural silvering
    hsv_roi[:, :, 1] = hsv_roi[:, :, 1] * (1.0 - (grey_factor * hair_mask))
    hsv_roi[:, :, 2] = np.clip(hsv_roi[:, :, 2] + (grey_factor * 40 * hair_mask), 0, 255)
    
    aged_hair = cv2.cvtColor(hsv_roi.astype(np.uint8), cv2.COLOR_HSV2RGB)
    
    out_img = img_rgb.copy()
    out_img[hair_top:hair_bottom, hair_left:hair_right] = aged_hair
    return out_img

def _apply_wrinkles_and_texture(img_rgb: np.ndarray, face_box: tuple, years: int) -> np.ndarray:
    """Generate smooth, natural facial aging folds and subtle skin texture maturity."""
    h, w, _ = img_rgb.shape
    x_min, y_min, x_max, y_max = face_box
    
    fx0, fy0 = max(0, x_min), max(0, y_min)
    fx1, fy1 = min(w, x_max), min(h, y_max)
    
    if fx1 <= fx0 or fy1 <= fy0:
        return img_rgb
        
    face_roi = img_rgb[fy0:fy1, fx0:fx1].copy()
    fh, fw, _ = face_roi.shape
    
    gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
    
    # 1. Soft morphological edge extraction
    kernel_size = max(5, int(min(fh, fw) * 0.06) | 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    
    # Smooth the extracted edges so there are no harsh black streaks
    blackhat = cv2.GaussianBlur(blackhat, (7, 7), 0)
    
    # 2. Focus texture on forehead and laugh lines smoothly
    wrinkle_mask = np.zeros((fh, fw), dtype=np.float32)
    wrinkle_mask[0:int(fh * 0.35), :] = 0.6
    wrinkle_mask[int(fh * 0.35):int(fh * 0.8), int(fw * 0.12):int(fw * 0.88)] = 0.5
    wrinkle_mask = cv2.GaussianBlur(wrinkle_mask, (31, 31), 0)
    
    # Gentle intensity (calibrated for natural realism)
    intensity = (years / 20.0) * 0.55
    darkening = (blackhat.astype(np.float32) * intensity * wrinkle_mask)[:, :, np.newaxis]
    
    aged_roi = face_roi.astype(np.float32) - darkening
    aged_roi = np.clip(aged_roi, 0, 255).astype(np.uint8)
    
    # 3. Soft blending with original skin tone to maintain natural beauty and recognition
    blended_roi = cv2.addWeighted(face_roi, 0.45, aged_roi, 0.55, 0)
    
    # 4. Subtle contrast enhancement
    pil_face = Image.fromarray(blended_roi)
    enhancer_contrast = ImageEnhance.Contrast(pil_face)
    pil_face = enhancer_contrast.enhance(1.0 + (years * 0.012))
    
    enhancer_sharpness = ImageEnhance.Sharpness(pil_face)
    pil_face = enhancer_sharpness.enhance(1.0 + (years * 0.015))
    
    out_img = img_rgb.copy()
    out_img[fy0:fy1, fx0:fx1] = np.array(pil_face)
    return out_img

def _apply_geometric_sagging(img_rgb: np.ndarray, face_box: tuple, years: int) -> np.ndarray:
    """Simulate subtle, natural lower-face jawline broadening."""
    h, w, _ = img_rgb.shape
    x_min, y_min, x_max, y_max = face_box
    
    fh = y_max - y_min
    fw = x_max - x_min
    
    src_pts = np.float32([
        [x_min, y_min],
        [x_max, y_min],
        [x_min, y_max],
        [x_max, y_max]
    ])
    
    sag_pixels = int(fh * (years * 0.0018))
    dst_pts = np.float32([
        [x_min, y_min],
        [x_max, y_min],
        [x_min - (fw * 0.012), y_max + sag_pixels],
        [x_max + (fw * 0.012), y_max + sag_pixels]
    ])
    
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img_rgb, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return warped

def simulate_age_progression(image_numpy: np.ndarray, years: int = 10) -> tuple:
    """
    Simulates smooth, natural, and realistic predictive facial age progression.
    Returns: (aged_image_numpy, aged_landmarks)
    """
    if image_numpy is None:
        return None, None

    h, w, _ = image_numpy.shape
    aged_img = image_numpy.copy()

    # 1. Extract base landmarks
    raw_landmarks = extract_face_mesh_landmarks(image_numpy)
    
    landmarks_dicts = []
    if raw_landmarks is not None and len(raw_landmarks) > 0:
        first_elem = raw_landmarks[0]
        if isinstance(first_elem, (float, int, np.floating)):
            for i in range(0, len(raw_landmarks) - 2, 3):
                landmarks_dicts.append({
                    "x": float(raw_landmarks[i]),
                    "y": float(raw_landmarks[i+1]),
                    "z": float(raw_landmarks[i+2])
                })
        elif isinstance(first_elem, dict):
            landmarks_dicts = raw_landmarks
        else:
            for lm in raw_landmarks:
                landmarks_dicts.append({
                    "x": float(getattr(lm, "x", 0)),
                    "y": float(getattr(lm, "y", 0)),
                    "z": float(getattr(lm, "z", 0))
                })

    # Compute bounding box
    if landmarks_dicts:
        xs = [int(lm["x"] * w) for lm in landmarks_dicts]
        ys = [int(lm["y"] * h) for lm in landmarks_dicts]
        face_box = (max(0, min(xs)), max(0, min(ys)), min(w, max(xs)), min(h, max(ys)))
    else:
        face_box = (int(w * 0.2), int(h * 0.2), int(w * 0.8), int(h * 0.8))

    # 2. Apply Smooth & Realistic Aging Transformations
    # A. Smooth Wrinkles & Skin Texture Aging
    aged_img = _apply_wrinkles_and_texture(aged_img, face_box, years)
    
    # B. Subtle Hair Greying & Highlight Shift (for +10Y and above)
    if years >= 10:
        aged_img = _apply_hair_greying(aged_img, face_box, years)
        
    # C. Natural Jawline Morphing
    aged_img = _apply_geometric_sagging(aged_img, face_box, years)

    # 3. Simulate age-progressed landmark coordinate shifts
    aged_landmarks = []
    for lm in landmarks_dicts:
        x, y, z = lm["x"], lm["y"], lm["z"]
        
        if y > 0.4:
            y_aged = y + (years * 0.0010)
        else:
            y_aged = y
            
        x_aged = x + ((x - 0.5) * (years * 0.002))
        aged_landmarks.append({"x": x_aged, "y": y_aged, "z": z})

    return aged_img, aged_landmarks
