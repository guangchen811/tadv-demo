# Test Resources

This directory contains example data and code for testing the TaDV constraint generation pipeline.

## Files

### Dataset
- **sample_bookings.csv** - Sample booking data with columns:
  - `name`: Customer name (textual, nullable)
  - `email`: Email address (textual, nullable)
  - `location`: Country code (categorical: US, EU, GER)
  - `guest_category_idx`: Guest category (numerical: 0-3)
  - `revenue`: Booking revenue (numerical)
  - `booking_status`: Status (categorical: COMPLETED, IN_PROGRESS, CANCELED)

### Task Code Examples

1. **batch_processing_task.py**
   - Sends discount emails to completed bookings
   - Uses Polars for data processing
   - Requires: `guest_category_idx` in range [0-3], `email` complete for COMPLETED bookings

2. **analytics_task.py**
   - Generates DuckDB report of active bookings
   - Robust task with minimal assumptions
   - Requires: `booking_status`, `guest_category_idx` columns present

3. **ml_task.py**
   - Trains logistic regression model
   - Uses sklearn with OneHotEncoder
   - Requires: `revenue` complete with non-zero std dev, `location` complete, `booking_status` has some COMPLETED values

## Usage

These resources are used in integration tests:

```bash
# Run integration tests with real LLM

# OpenAI
RUN_LLM_TESTS=1 OPENAI_API_KEY=sk-... uv run pytest tests/integration/ -v -s

# Anthropic
RUN_LLM_TESTS=1 ANTHROPIC_API_KEY=sk-ant-... uv run pytest tests/integration/ -v -s

# Google Gemini
RUN_LLM_TESTS=1 GOOGLE_API_KEY=... uv run pytest tests/integration/ -v -s

# Override default model
RUN_LLM_TESTS=1 GOOGLE_API_KEY=... LLM_MODEL=gemini/gemini-2.5-flash uv run pytest tests/integration/ -v -s
```

## Expected Constraints

### Batch Processing Task
- `guest_category_idx` completeness
- `guest_category_idx` range [0-3]
- `email` completeness where `booking_status='COMPLETED'`

### Analytics Task
- `booking_status` completeness
- `guest_category_idx` completeness

### ML Task
- `revenue` completeness
- `revenue` std dev != 0
- `location` completeness
- `location` in set [US, EU, GER]
- `booking_status` has COMPLETED values
