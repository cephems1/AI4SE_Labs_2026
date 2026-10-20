#!/usr/bin/env python3
"""Run the requirements-refinement network on a directory of input documents.

Usage:
    python run.py data/corpus                      # writes output/requirements.md + .json
    python run.py data/corpus -o out --model extract=gpt-4.1-nano --model review=gpt-5-mini
    python run.py --graph-only                      # only writes the Mermaid diagram of the graph
"""

import argparse
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
ROLES = ("extract", "completeness", "taxonomy", "consolidate", "review", "revise")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", nargs="?", help="directory with the input documents (searched recursively)")
    parser.add_argument("-o", "--output-dir", default=str(HERE / "output"))
    parser.add_argument("--model", action="append", default=[], metavar="ROLE=MODEL",
                        help=f"override the model of a role ({', '.join(ROLES)})")
    parser.add_argument("--graph-only", action="store_true", help="only export the graph diagram")
    args = parser.parse_args()

    load_dotenv(HERE / ".env")
    load_dotenv()
    for spec in args.model:
        role, _, model = spec.partition("=")
        if role not in ROLES or not model:
            parser.error(f"invalid --model {spec!r}; roles: {', '.join(ROLES)}")
        os.environ[f"RN_MODEL_{role.upper()}"] = model

    from requirements_network.config import MAX_CONCURRENCY
    from requirements_network.graph import build_graph

    graph = build_graph()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.mmd").write_text(graph.get_graph().draw_mermaid(), encoding="utf-8")
    if args.graph_only:
        print(f"Graph written to {out_dir / 'graph.mmd'}")
        return
    if not args.input_dir:
        parser.error("input_dir is required")
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit(f"OPENAI_API_KEY is not set. Put it into {HERE / '.env'} (see .env.example).")

    start = time.time()
    final = graph.invoke({"input_dir": str(Path(args.input_dir).resolve()), "output_dir": str(out_dir.resolve())},
                         config={"recursion_limit": 200, "max_concurrency": MAX_CONCURRENCY})
    print(f"\nDone in {time.time() - start:.0f}s: {len(final['requirements'])} requirements, "
          f"{len(final['blacklist'])} discarded.")
    for kind, path in final["outputs"].items():
        print(f"  {kind}: {path}")


if __name__ == "__main__":
    main()
