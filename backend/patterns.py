from .observer.pattern_detector import PatternDetector

def pattern_summary(snapshots): return PatternDetector().detect(snapshots)
