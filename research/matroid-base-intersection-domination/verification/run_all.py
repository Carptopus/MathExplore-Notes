"""串行、固定范围的端到端复现入口；任何失败立即停止，不重试。"""

import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
if sys.platform != 'win32':
    raise RuntimeError('复现实现需要Windows和Python>=3.10；不是跨平台软件声明')
if sys.version_info < (3, 10) or not __debug__:
    raise RuntimeError('需要Python>=3.10且不得使用 -O / -OO')

COMMANDS = [
    ('connection', ['check_connection_law.py']),
    ('frontier', ['check_cover_frontier.py']),
    ('laminar', ['check_deepening.py']),
    ('output', ['laminar_solver.py', '--input', 'simple_rank4_q5.json']),
    ('binary', ['verify_fixed_witnesses.py', '--no-write']),
]


def main():
    report = []
    for name, args in COMMANDS:
        start = time.monotonic()
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', *args],
                                cwd=HERE, capture_output=True, text=True,
                                encoding='utf-8', timeout=55, check=True)
        evidence = json.loads(result.stdout)
        if name == 'connection':
            if evidence['nonmatroid_negative']['P6_cost'] != 2:
                raise AssertionError('非拟阵负控失败')
        elif name == 'frontier':
            if not evidence['fixed_controls'] or any(
                    row['result'] != 'PASS' for row in evidence['fixed_controls']):
                raise AssertionError('覆盖前沿固定复核失败')
        elif name == 'laminar':
            if evidence['status'] != 'VERIFIED' or evidence['stats']['cycle'] < 1:
                raise AssertionError('Laminar复核或关联圈正控失败')
        elif name == 'output':
            if evidence['gamma_ck'] != 6 or len(evidence['bases']) != 6:
                raise AssertionError('32元素固定输出失败')
        elif name == 'binary':
            if evidence['status'] != 'PASS_FIXED_ONLY' or len(evidence['negative_controls']) != 4:
                raise AssertionError('二元固定复核失败')
        report.append({'name': name, 'elapsed_seconds': time.monotonic() - start,
                       'evidence': evidence})
    print(json.dumps({'status': 'VERIFIED_FIXED_SCOPE_ONLY', 'runs': report,
                      'boundary': '有限复核；不证明一般量词，不确认首发；无完整大图枚举'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
