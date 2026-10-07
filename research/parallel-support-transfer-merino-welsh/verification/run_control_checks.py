"""运行冻结的七个原对象控制并检查失败行为；不承担一般证明。"""

from __future__ import annotations

import copy
import json
import time
from pathlib import Path

import verify_transfer_controls as verifier


def compare(actual, expected):
    if actual != expected:
        raise ValueError("冻结结果比较失败")


def main():
    started = time.monotonic()
    rows = [
        verifier.vector_case("independent_support", (1, 1, 1, 2, 2, 2, 4, 5, 6, 7), range(6), 3),
        verifier.vector_case("internal_singleton", (1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7), range(7), 3),
        verifier.vector_case("dependent_support", (1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7), range(9), 3),
        verifier.vector_case("internal_small_class", (1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7), range(8), 3),
        verifier.vector_case("equality_parallel_pair", (1, 1), range(2), 2),
        verifier.theta_case(4, 3, 3, True),
        verifier.theta_case(4, 2, 2, False),
    ]
    count = sum(row["subsets"] for row in rows)
    if count >= 100_000:
        raise ValueError("固定范围超过资源门")
    fixture = json.loads((Path(__file__).parent / "results" / "transfer_s2.json").read_text(encoding="utf-8"))
    compare(rows, fixture["cases"])
    compare(count, fixture["subsets_checked"])
    try:
        verifier.theta_case(4, 2, 2, True)
    except ValueError as error:
        if "前提控制不符" not in str(error):
            raise
    else:
        raise ValueError("负控错误地通过了过度推广")
    broken = copy.deepcopy(rows)
    broken[0]["T02"] += 1
    try:
        compare(broken, fixture["cases"])
    except ValueError:
        pass
    else:
        raise ValueError("破坏性结果比较未失败")
    elapsed = time.monotonic() - started
    if elapsed > 60:
        raise ValueError("固定验证超过60秒资源门")
    print(json.dumps({"status": "VERIFIED", "cases": len(rows), "subsets": count,
                      "negative_and_destructive_controls": "passed", "seconds": round(elapsed, 3)}))


if __name__ == "__main__":
    main()
