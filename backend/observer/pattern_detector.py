"""Privacy-safe pattern detector operating only on metadata snapshots."""
from collections import Counter
from datetime import datetime
class PatternDetector:
    def detect(self, snapshots):
        if len(snapshots)<3: return []
        apps=[s.app_name for s in snapshots if s.app_name]
        counts=Counter(apps); total=len(apps)
        out=[]
        for app,n in counts.most_common(8):
            if n>=3: out.append({'kind':'repetition','description':f'You frequently use {app}','confidence':round(n/total*100,1),'evidence_count':n})
        for a,b in zip(apps,apps[1:]):
            if a!=b: out.append({'kind':'context_switch','description':f'{a} → {b} is a recurring transition','confidence':50.0,'evidence_count':1})
        return out[:20]
