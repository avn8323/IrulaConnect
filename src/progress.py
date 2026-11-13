import json
from pathlib import Path
from datetime import datetime, timezone
from .config import PROGRESS_PATH

def _blank():
    return {'attempted': [], 'known': [], 'revision': [], 'saved': [], 'last_practice': None, 'last_visit': None, 'total_seconds': 0, 'section_known': {}, 'session_started': None}

def load_progress(path=None):
    p=Path(path) if path else PROGRESS_PATH
    if not p.exists(): return _blank()
    try:
        data=json.loads(p.read_text(encoding='utf-8'))
        state=_blank(); state.update(data if isinstance(data,dict) else {})
        for k in ('attempted','known','revision','saved'):
            if not isinstance(state.get(k),list): state[k]=[]
        return state
    except (json.JSONDecodeError,OSError): return _blank()

def save_progress(state,path=None):
    p=Path(path) if path else PROGRESS_PATH
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    return state

def update_progress(record_id,action,path=None,section=None):
    state=load_progress(path)
    if action not in ('attempted','known','revision','saved','unsave','unlearn'):
        raise ValueError('Unsupported progress action.')
    if action=='unsave': state['saved']=[x for x in state['saved'] if x!=record_id]
    elif action=='unlearn': state['known']=[x for x in state['known'] if x!=record_id]
    elif record_id not in state[action]: state[action].append(record_id)
    state['last_practice']=datetime.now(timezone.utc).isoformat()
    if section and action in ('known','unlearn'):
        state.setdefault('section_known',{})[section]=len(state['known'])
    return save_progress(state,path)

def record_visit(path=None):
    state=load_progress(path); now=datetime.now(timezone.utc).isoformat(); state['last_visit']=now
    if not state.get('session_started'): state['session_started']=now
    return save_progress(state,path)

def add_session_seconds(seconds, path=None):
    """Accumulate active foreground time in the local progress file."""
    try: seconds=max(0,int(seconds))
    except (TypeError,ValueError): seconds=0
    if not seconds: return load_progress(path)
    state=load_progress(path)
    state['total_seconds']=int(state.get('total_seconds',0))+seconds
    return save_progress(state,path)
