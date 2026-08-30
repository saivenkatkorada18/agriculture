# Workflow: Add Crop Class (`/add-crop-class`)

Follow these sequential steps when extending the plant disease class registry with a new crop or disease:

1. **Update ML Metadata**:
   - Add the new crop disease entry in `ml/models/disease_info.json`.
   - Ensure the entry includes `crop`, `disease_name`, `scientific_name`, `symptoms`, `causes`, `organic_treatment`, `chemical_treatment`, and `prevention_tips`.

2. **Update Class List**:
   - Add the class identifier to `ml/config/config.py` in `SUPPORTED_CLASSES`.

3. **Update Frontend Constants & Types**:
   - Verify `frontend/lib/constants.ts` includes the crop in filter lists and sample selector.

4. **Verify Inference & Test**:
   - Run `pytest backend/tests/test_analysis.py` to ensure prediction and recommendation logic maps correctly without KeyError.

5. **Commit with Conventional Commit**:
   - `git commit -m "feat(ml): add [Crop Name] [Disease Name] class and treatment guide"`
