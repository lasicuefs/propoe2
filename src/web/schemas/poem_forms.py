from pydantic import BaseModel

from .prosody import Prosody
from .weights import Weights

class Entry(BaseModel):
    """Entry Scheme for the /poem/ endpoint"""

    prosody: Prosody
    weights: Weights
