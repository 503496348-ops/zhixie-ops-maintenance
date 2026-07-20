# langgenius/dify

- 目标状态：`pending_review -> implementation-ready`
- 入口 Commit：`f93a5b95c65e7e4b5a3c7cc8057bf27a3a4aba50`
- 备选：`6022939bf0fab20eef9449284f806b0896959e97`, `30df1433cc511c6c19f2cd60afef77996a40edad`
- 映射产品：`hermes-doctor`, `pipixia-doctor`

## 1) 后端能力线
- 源文件：`api/services/dataset_service.py`, `api/controllers/console/explore/trial.py`, `api/controllers/console/files.py`
- 抽取能力：dataset 事务提交、租户隔离、异常回滚
- 产物：`hermes-doctor/services/dataset_service_adapter.py`
- 验收：
  - `pytest -q api/tests/unit_tests/services/test_dataset_service_dataset.py`
  - `pytest -q api/tests/unit_tests/controllers/console/explore/test_trial.py api/tests/unit_tests/controllers/console/test_files.py`

## 2) 前端能力线
- 源文件：`web/app/components/workflow/workflow-preview/index.tsx`, `web/app/components/plugins/plugin-auth/authorize/permission-selector.tsx`, `web/app/components/base/permission-selector/index.tsx`
- 抽取能力：workflow 预览状态收口、权限选择交互
- 产物：`pipixia-doctor/components/common/permission-selector.tsx`（含 Hook）
- 验收：
  - `cd /root/projects/hermes-doctor && npm test -- --runInBand`
  - `cd /root/projects/pipixia-doctor && npm test -- --runInBand`

## 下一拍动作
- 将两条能力线拆成两张 implementation 小工单，附回退点；完成 smoke 后再落 `implemented`。