# 资源架构

阅读记录包含章笔记、批次、复算、定位和核验；投资框架包含去个人化流程、完整专题与执行资料。catalog.json按路径、书号、类型和指纹路由；manifest.json登记全部公开文件，二者由scripts/update_catalog.py显式重建。

此库与Skill分别发布。Skill使用resources.lock.json锁定本库commit及manifest/catalog指纹。完整安装把同一快照置于技能目录的resources/library；远程安装按目录读取固定commit的相关文件。用户工作区保存IPS、自有资料、报告与实际引用记录。历史IPS关联叙述不公开，文件/节号关系单列纯映射表；首版495项资料及506个文件。原书及维护者私人主库不参与运行依赖。
