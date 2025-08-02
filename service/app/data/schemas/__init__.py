# Import all models so SQLAlchemy can discover them
from .assessments import Assessment
from .candidates import Candidate, CandidateAttempt 
from .recordings import Recording