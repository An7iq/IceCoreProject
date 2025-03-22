import pandas as pd
from volcano_detection.config import SIGL2015_PATH, GVP_PATH, ICECORE_PATH
from volcano_detection.utils.matching import match_events
import os

def load_data():
    print("📦 Loading datasets...")
    icecore_df = pd.read_csv(ICECORE_PATH)
    gvp_df = pd.read_csv(GVP_PATH)
    sigl_df = pd.read_csv(SIGL2015_PATH)
    print(f"✅ Icecore shape: {icecore_df.shape}")
    print(f"✅ GVP shape: {gvp_df.shape}")
    print(f"✅ Sigl2015 shape: {sigl_df.shape}")
    return icecore_df, gvp_df, sigl_df

def preprocess_gvp(gvp_df):
    print("🧹 Preprocessing GVP...")
    gvp_df = gvp_df[gvp_df['Last Known Eruption'] != 'Unknown'].copy()
    gvp_df['year'] = gvp_df['Last Known Eruption'].str.extract(r'(\d+)').astype(float)
    score_map = {
        'Observed': 2,
        'Credible': 1,
        'Uncertain': -1,
        'Unrest': -2
    }
    gvp_df['reliability_score'] = gvp_df['Activity Evidence'].map(score_map).fillna(0)
    return gvp_df

def preprocess_sigl(sigl_df, cooling_path="volcano_detection/data/sigl2015_cooling_support.csv"):
    print("🧹 Enhancing Sigl2015 with cooling support...")
    if os.path.exists(cooling_path):
        cooling_df = pd.read_csv(cooling_path)
        cooling_years = set()
        for events in cooling_df['volcanic_events']:
            cooling_years.update([int(e.strip()) for e in str(events).split(',') if e.strip().lstrip('-').isdigit()])
        sigl_df['cooling_score'] = sigl_df['year'].apply(lambda y: 1 if y in cooling_years else 0)
    else:
        sigl_df['cooling_score'] = 0
    sigl_df['total_score'] = 1 + sigl_df['cooling_score']  # 默认+1为事件存在，加冷却加分
    return sigl_df

def label_icecore(icecore_df, gvp_df, sigl_df, tolerance=1):
    print("🏷️ Labeling volcanic events in ice core data...")
    icecore_df['year'] = icecore_df['b2k_age'].round()
    icecore_df['gvp_match'] = icecore_df['year'].isin(gvp_df['year'])
    icecore_df['sigl_match'] = icecore_df['year'].isin(sigl_df['year'])
    icecore_df['label'] = 0
    icecore_df.loc[icecore_df['gvp_match'], 'label'] += 1
    icecore_df.loc[icecore_df['sigl_match'], 'label'] += 1
    return icecore_df

def main():
    icecore_df, gvp_df, sigl_df = load_data()
    gvp_df = preprocess_gvp(gvp_df)
    sigl_df = preprocess_sigl(sigl_df)
    icecore_labeled = label_icecore(icecore_df, gvp_df, sigl_df)
    print("📊 Sample labeled icecore data:")
    print(icecore_labeled[['b2k_age', 'label', 'gvp_match', 'sigl_match']].head(10))

if __name__ == "__main__":
    main()
