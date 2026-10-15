#!/usr/bin/env python3
"""维护者显式登记公共资源及指纹；不推断或升级阅读状态。只用Python标准库。"""
from pathlib import Path
import argparse, hashlib, json, re


def update(root,version):
    root=Path(root).resolve()
    entries=[]
    for folder in ('阅读记录','投资框架'):
        for p in sorted((root/folder).rglob('*')):
            if p.is_symlink():raise ValueError('资源不能为符号链接')
            if not p.is_file():continue
            if p.suffix not in ('.md','.json'):raise ValueError('只允许笔记、记录和方法文本')
            name=p.relative_to(root).as_posix();b=p.read_bytes()
            if p.suffix=='.json':json.loads(b)
            books=sorted(set(re.findall(r'B\d{2,}',p.name)))
            entries.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                            'book_ids':books,'kind':'chapter_note' if '逐章笔记' in p.parts else 'batch_record' if '批次记录' in p.parts else 'method' if folder=='投资框架' else 'reading_record',
                            'reading_status':'见该文件的实际记录；新增文件不自动视为已读或已核验'})
    catalog={'schema_version':1,'resource_version':version,'files':entries,
             'reading_progress':'阅读记录/逐段精读进度.json','bibliography':'阅读记录/书籍结构索引.json',
             'limitations':'原书、解码全文、图像和私有资料未提供。历史状态为继承记录，不是当前Agent实读证明。'}
    (root/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    manifest=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(x.startswith('.') or x=='__pycache__' for x in rel.parts) or not p.is_file() or rel.as_posix()=='manifest.json':continue
        if p.is_symlink():raise ValueError('不能包含链接')
        b=p.read_bytes();manifest.append({'path':rel.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    value={'schema_version':1,'name':'invest-resources','version':version,'files':manifest}
    (root/'manifest.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    return {'status':'PASS','resources':len(entries),'files':len(manifest)+1,'version':version}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--version',required=True)
    args=parser.parse_args();print(json.dumps(update(Path(__file__).resolve().parents[1],args.version),ensure_ascii=False))
