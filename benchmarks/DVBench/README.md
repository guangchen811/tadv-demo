# DVBench: End-to-End Error Impact Detection Benchmark

## Overview

DVBench evaluates the ability of data validation systems to detect errors that impact downstream task execution. Unlike
ICDBench (which tests constraint discovery), DVBench measures end-to-end error impact: **does a data validation system
correctly predict whether a data batch will cause a task to fail?**

**Quick Facts:**

- 5 datasets from diverse domains
- 60 downstream task scripts (Python)
- 25 error injection configurations per dataset
- Each task contains executable assertion blocks as ground truth
- Managed via [project_manager](../../tadv/project_manager) for task execution

## Datasets

| Dataset            | Source | Domain               | # Columns | # Tasks |
|--------------------|--------|----------------------|-----------|---------|
| students           | UCI ML | Academic performance | 37        | 10      |
| hr_analytics       | Kaggle | Employee attrition   | 38        | 12      |
| sleep_health       | Kaggle | Sleep & lifestyle    | 13        | 13      |
| IPL_win_prediction | Kaggle | Cricket matches      | 20        | 15      |
| imdb               | Kaggle | Movies & TV shows    | 16        | 10      |

## Component Description

### 1. `files/` - Clean Data

- **`data.csv`**: Original clean dataset (D_sample)
- Used for task development and constraint generation
- Contains valid data that satisfies all task assumptions

### 2. `scripts/` - Downstream Tasks

- **Task scripts**: Python files that consume data and produce outputs
- **Format**: Each script takes `--input` (data directory) and `--output` (result directory)
- **Assertion blocks**: Embedded ground truth checks (delimited by `# ASSERTION_START` / `# ASSERTION_END`)
    - Enable programmatic validation of task assumptions
    - Removed during constraint generation (to prevent leakage)
    - Used during evaluation to determine ground truth labels

**Example Script Structure:**

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(args.input, 'new_data.csv'))

    # ASSERTION_START
    assert df['enrolled'].notna().all(), "enrolled must be complete"
    assert (df['approved'] <= df['enrolled']).all(), "approved <= enrolled"
    # ASSERTION_END

    # Task logic...
    result = compute_something(df)
    result.to_csv(os.path.join(args.output, 'result.csv'))
```

### 3. `errors/` - Error Injection Configurations

- **25 YAML files per dataset**: Define synthetic error injections
- Each configuration specifies:
    - Error operator (e.g., `ColumnInserting`, `MaskValues`, `GaussianNoise`)
    - Target columns
    - Severity parameters
    - Sampling strategy

**Example Error Config:**

```yaml
- ColumnInserting:
    Columns:
      - Target
    Params:
      severity: 0.1
      sampling: CAR
      corrupt_strategy: add_prefix
```

Error operators are implemented in [tadv/error_injection](../../tadv/error_injection).

### 4. `annotations/` - Ground Truth (Optional)

- Additional annotations for specific tasks

### 5. `scripts/metadata.yaml` - Dataset Metadata

- Dataset source URL
- Table name

## Task Execution via Project Manager

Tasks are executed using the [project_manager](../../tadv/project_manager) which:

1. Strips assertion blocks from task code
2. Applies error injection configurations to create new data batches
3. Executes tasks with clean data (baseline) and error-injected data
4. Compares results against assertion blocks to determine ground truth labels

## Ground Truth Labeling

For each (task, data batch) pair:

- **Safe (label = 1)**: Task executes successfully, all assertions pass
- **Erroneous (label = 0)**: Task crashes OR any assertion fails

## Evaluation Protocol

1. **Input**: Clean data (D_sample) + Task code (with assertions stripped)
2. **Generate Constraints**: System produces data validation rules
3. **Apply to Error Batches**: Validate each of 25 error-injected batches
4. **Compare Predictions**:
    - System predicts: PASS (safe) or FAIL (erroneous)
    - Ground truth: Execute task with assertions enabled
5. **Metrics**: Precision, Recall, F1 score

## Dataset Generation

The 60 tasks in DVBench were generated using an **LLM-assisted, human-in-the-loop pipeline** described in **Section 6.2
** of the paper.

**Documentation**:

- **Generation pipeline**: [workflow_tadv/eid_bench_building/](../../workflow_tadv/eid_bench_building/) -
  Scripts and methodology
- **Intermediate outputs**: [eid_bench_gen/](../../eid_bench_gen/) - Generated tasks before final selection
