import os
import sys
import traceback
from dotenv import load_dotenv
load_dotenv('.env', override=True)

# Ensure current path is in sys.path
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from langchain_openai import ChatOpenAI

try:
    LLM_INSTANCES = {
        "GPT_5": {
            "MODEL": ChatOpenAI(
                    model="gpt-5",
                    timeout=None,
                )
        }
        ,
        "GPT_4_1": {
            "MODEL": ChatOpenAI(
                    model="gpt-4.1",
                    temperature=0,
                )
        }
        ,
        "GPT_5_MINI": {
            "MODEL": ChatOpenAI(
                    model="gpt-5-mini",
                    temperature=0,
                    timeout=None,
                )
        }
        ,
        "GPT_5_NANO": {
            "MODEL": ChatOpenAI(
                    model="gpt-5-nano",
                    timeout=None,
                )
        }
    }
except Exception as _exp:
    print("Exception occurred while loading LLM instances:")
    traceback.print_exc()