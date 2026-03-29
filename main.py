import os
import sys
import uvicorn
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main():
    uvicorn.run(
        "src.app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )


if __name__ == "__main__":
    main()
