"""串行原矩阵独立重构；完成32项才生成完整证据，不自动重试。"""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent; root=here.parents[2]
    target=args.output.resolve()
    if target.parent!=(here/'results').resolve() or target.exists():
        raise ValueError('必须用本案例results直接目录中的新证据文件名')
    checker=here/'small_shape_independent_checker.py'
    runner=root/'loops/LOGBM3-RECOVERY-GATE-0002/bounded_symbolic_run.py'
    work=Path(tempfile.mkdtemp(prefix='s32-independent-',dir=root/'tmp'))
    records=[]
    for index in range(32):
        command=[sys.executable,'-B','-X','utf8',str(runner),'--seconds','50','--mib','128',
                 str(checker),'--packet',str(args.packet.resolve()),'--case-index',str(index),
                 '--output',str(work/f'case-{index}.json')]
        result=subprocess.run(command,cwd=root,capture_output=True,text=True,encoding='utf-8')
        if result.returncode:
            raise RuntimeError(f'独立复核停止，不重试：index={index}\n{result.stdout}\n{result.stderr}')
        lines=result.stdout.splitlines()
        receipt=json.loads(next(line for line in lines if line.startswith('{')))
        certificate=json.loads(Path(receipt['output']).read_text(encoding='utf-8'))
        resource=ast.literal_eval(next(line.removeprefix('RESOURCE_SUMMARY ') for line in lines if line.startswith('RESOURCE_SUMMARY ')))
        if resource['gate'] is not None or certificate['status']!='VERIFIED_FROM_ORIGINAL_MATRIX':
            raise RuntimeError('独立证书或资源门失败，不重试')
        records.append({'certificate':certificate,'resource':resource})
        print(json.dumps({'completed':index+1,'of':32,'case':certificate['case'],'seconds':resource.get('seconds')}),flush=True)
    packet={'scope':'COMPLETE_N3_TO_7_NONSTAR_GROUPED_CONTINUOUS_DOMAIN',
            'discovery_sha256':hashlib.sha256(args.packet.read_bytes()).hexdigest(),
            'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),
            'coefficient_order':'lexicographic product range(degree_i+1)',
            'status':'INDEPENDENT_EXACT_CERTIFICATES_REQUIRES_MATHEMATICAL_AUDIT',
            'cases':records}
    target.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'complete':32,'output':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
