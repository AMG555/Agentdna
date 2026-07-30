import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from backend.observer.privacy_guard import PrivacyGuard
from backend.agents import Agent
from backend.observer.pattern_detector import PatternDetector
from backend.observer.activity_monitor import ActivitySnapshot
from backend.ai.providers import EmbeddingProvider, LLMProvider, ProviderError
from backend.ai.structured import parse_model_json
from backend.ai.model_router import ModelRouter
from backend.privacy.redaction import redact
from backend.nursery import Nursery
from backend.automation_executor import AutomationExecutor
import os
from backend.retrieval.vector_store import LocalVectorStore
from backend.reasoning.react_loop import ReactLoop

class PrivacyTests(unittest.TestCase):
    def test_safe_default_blocks_everything(self):
        g=PrivacyGuard(); self.assertFalse(g.monitoring_enabled); self.assertFalse(g.can_capture('Code'))
    def test_requires_allowlist_and_blocks_sensitive_apps(self):
        g=PrivacyGuard(); g.allow('Code'); g.resume(); self.assertTrue(g.can_capture('Code')); self.assertFalse(g.can_capture('Password Manager'))
    def test_pause_is_immediate(self):
        g=PrivacyGuard(); g.allow('Code'); g.resume(); g.pause(); self.assertFalse(g.can_capture('Code'))

class AgentTests(unittest.TestCase):
    def test_accept_increases_fitness(self):
        a=Agent('x','Test','shortcut','trigger','action'); old=a.fitness; a.feedback('ACCEPTED'); self.assertEqual(a.fitness,old+15)
    def test_never_kills_agent(self):
        a=Agent('x','Test','shortcut','trigger','action'); a.feedback('NEVER'); self.assertEqual(a.state,'DEAD')
    def test_fitness_is_clamped(self):
        a=Agent('x','Test','shortcut','trigger','action',99); a.feedback('THUMBS_UP'); self.assertEqual(a.fitness,100)

class ProviderTests(unittest.TestCase):
    def test_openrouter_status_never_exposes_key(self):
        old={k:os.environ.get(k) for k in ('AGENTDNA_LLM_MODE','AGENTDNA_LLM_API_KEY')}
        os.environ['AGENTDNA_LLM_MODE']='openrouter'; os.environ['AGENTDNA_LLM_API_KEY']='secret-test-key'
        try:
            status=LLMProvider().status(); self.assertTrue(status['api_key_configured']); self.assertNotIn('secret-test-key',str(status))
        finally:
            for k,v in old.items():
                if v is None: os.environ.pop(k,None)
                else: os.environ[k]=v
    def test_cloud_provider_requires_key_before_network(self):
        old={k:os.environ.get(k) for k in ('AGENTDNA_LLM_MODE','AGENTDNA_LLM_API_KEY')}
        os.environ['AGENTDNA_LLM_MODE']='openrouter'; os.environ.pop('AGENTDNA_LLM_API_KEY',None)
        try:
            with self.assertRaises(ProviderError): LLMProvider().generate('test')
        finally:
            for k,v in old.items():
                if v is None: os.environ.pop(k,None)
                else: os.environ[k]=v

class SafetyTests(unittest.TestCase):
    def test_redaction_removes_email_card_and_secret(self):
        out=redact('a@example.com 4111 1111 1111 1111 api_key_abcdefghijk')
        self.assertNotIn('a@example.com',out); self.assertNotIn('4111',out); self.assertNotIn('api_key_',out)
    def test_nursery_graduates_accurate_trial(self):
        n=Nursery(); n.start('a')
        for _ in range(10): n.observe('a',True)
        self.assertEqual(n.trials['a'].state,'GRADUATE')
    def test_automation_is_preview_only(self):
        result=AutomationExecutor().execute('open_url','https://example.com',True)
        self.assertFalse(result['executed'])

class AIOutputTests(unittest.TestCase):
    def test_invalid_model_output_becomes_safe_suggestion(self):
        result=parse_model_json('not-json'); self.assertTrue(result['requires_confirmation']); self.assertEqual(result['action_type'],'suggest_text')
    def test_unknown_action_is_downgraded(self):
        result=parse_model_json('{"suggestion":"x","action_type":"run_shell"}'); self.assertEqual(result['action_type'],'suggest_text')
    def test_sensitive_tasks_route_local(self): self.assertEqual(ModelRouter().choose('suggestion',sensitive=True),'local')

class RetrievalTests(unittest.TestCase):
    def test_embedding_is_deterministic(self):
        p=EmbeddingProvider(); self.assertEqual(p.embed('same text'),p.embed('same text'))
    def test_vector_search_ranks_related_text(self):
        s=LocalVectorStore(); s.add('a','python api documentation'); s.add('b','recipe for soup'); self.assertEqual(s.search('python api')[0]['id'],'a')
    def test_react_plan_is_bounded_and_allowlisted(self):
        plan=ReactLoop(max_steps=2).plan('open docs','coding context'); self.assertLessEqual(len(plan['steps']),2); self.assertTrue(plan['steps'][0]['authorized'])

class PatternTests(unittest.TestCase):
    def test_repeated_app_creates_pattern(self):
        snapshots=[ActivitySnapshot(str(i),'Code','file',10) for i in range(3)]
        result=PatternDetector().detect(snapshots); self.assertTrue(any(p['kind']=='repetition' for p in result))
    def test_small_input_is_empty(self): self.assertEqual(PatternDetector().detect([]),[])

if __name__=='__main__': unittest.main()
