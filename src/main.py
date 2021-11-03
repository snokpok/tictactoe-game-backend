import uvicorn
from server import run_app
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Mode ('dev', 'prod')", type=str, choices=["dev", 'prod'], default="dev")
    args = parser.parse_args()
    app = run_app(args.mode)
    uvicorn.run(app, host="0.0.0.0", port=4000)
